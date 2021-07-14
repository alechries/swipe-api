from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from . import filters as my_filter
from rest_framework import generics, request
from django_filters import rest_framework as filters

from .permissions import IsOwnerOrSuperuserOrReadOnly


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
