import jwt
from django.conf import settings
from django.contrib.auth import user_logged_in
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import jwt_payload_handler

from . import models, auth
from . import serializers
from . import filters as my_filter
from rest_framework import generics, request
from django_filters import rest_framework as filters
from .permissions import IsOwnerOrSuperuserOrReadOnly
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
import base64
from twilio.rest import Client
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from .serializers import RegistrationSerializer


class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']
        print(email, password)

        user = auth.EmailAuthBackend.authenticate(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload)
                user_details = {}
                user_details['name'] = (
                    user.first_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = serializers.UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GenerateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class PhoneNumberRegistered(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = models.PhoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            models.PhoneModel.objects.create(
                Mobile=phone,
            )
        Mobile = models.PhoneModel.objects.get(Mobile=phone)  # user Newly created Model
        if Mobile.isVerified == 0:
            Mobile.counter += 1  # Update Counter At every Call
            Mobile.save()  # Save the data
            keygen = GenerateKey()
            key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
            OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
            print(OTP.at(Mobile.counter))
            # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
            account_sid = 'AC6f35f826e5cda2eecb974aea4f10ac7b'
            auth_token = '27d56e82e0e4f6e7285be4d4ed604bd8'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=f'Ваш проверочный код. Срок действия - 5 минут {OTP.at(Mobile.counter)}',
                from_='+14322965747',
                to=f'+{Mobile.Mobile}'
            )
            OTP.at(Mobile.counter)
            return Response({"msg": "Сообщение отправлено"}, status=200)  # Just for demonstration
        else:
            return Response({"msg": "Телефон успешно активирован"}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = models.PhoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = GenerateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
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
