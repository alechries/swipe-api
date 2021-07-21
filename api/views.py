from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from . import filters as my_filter
from rest_framework import generics, request
from django_filters import rest_framework as filters
from .permissions import IsOwnerOrSuperuserOrReadOnly
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
import base64
from twilio.rest import Client




class GenerateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


EXPIRY_TIME = 300  # seconds


class PhoneNumberRegistered(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = models.PhoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            models.PhoneModel.objects.create(
                Mobile=phone,
                user_id=request.user.id
            )
        Mobile = models.PhoneModel.objects.get(Mobile=phone)  # user Newly created Model
        if Mobile.isVerified == 0:
            Mobile.counter += 1  # Update Counter At every Call
            Mobile.save()  # Save the data
            keygen = GenerateKey()
            key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
            OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)  # HOTP Model for OTP is created
            print(OTP.at(Mobile.counter))
            # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
            account_sid = 'AC6f35f826e5cda2eecb974aea4f10ac7b'
            auth_token = '35a9dfebd77bcdd432bc2431ed8f661f'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body= f'Ваш проверочный код. Срок действия - 5 минут {OTP.at(Mobile.counter)}',
                from_='+14322965747',
                to=f'+{Mobile.Mobile}'
            )
            OTP.at(Mobile.counter)
            return Response("Сообщение отправлено", status=200)  # Just for demonstration
        else:
            return Response("Номер уже верефицирован", status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = models.PhoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = GenerateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)  # HOTP Model
        if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("Верификация прошла успешно", status=200)
        return Response("OTP is wrong", status=400)


class ApartmentList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ApartmentListSerializer
    queryset = models.Apartment.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = my_filter.ApartmentFilter


class ApartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrSuperuserOrReadOnly, IsAuthenticated]
    queryset = models.Apartment.objects.all()
    serializer_class = serializers.ApartmentDetailSerializer


class ApartmentCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ApartmentCreateSerializer

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class FloorCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.FloorCreateSerializer


class FloorList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ApartmentListSerializer
    queryset = models.Floor.objects.all()


class ContactList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = serializers.ContactListSerializer
    queryset = models.Contact.objects.all()
    filterset_class = my_filter.ContactListFilter


class ContactCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ContactCreateSerializer

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class ContactUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrSuperuserOrReadOnly, IsAuthenticated]
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = models.User.objects.all()


class UserCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer


class PromoCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PromotionSerializer


class HouseList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HouseListSerializer
    queryset = models.House.objects.all()


class HouseCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HouseDetailSerializer


class HouseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrSuperuserOrReadOnly, IsAuthenticated]
    serializer_class = serializers.HouseDetailSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = models.House.objects.all()
