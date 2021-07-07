from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from . import filters as my_filter
from rest_framework import generics, request
from django_filters import rest_framework as filters


class ApartmentList(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ApartmentListSerializer
    queryset = models.Apartment.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = my_filter.ApartmentFilter


class ApartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ApartmentDetailSerializer
    queryset = models.Apartment.objects.all()


class ApartmentCreate(generics.CreateAPIView):
    serializer_class = serializers.ApartmentCreateSerializer


class FloorCreate(generics.CreateAPIView):
    serializer_class = serializers.FloorCreateSerializer


class FloorList(generics.ListAPIView):
    serializer_class = serializers.ApartmentListSerializer
    queryset = models.Floor.objects.all()


class ContactList(generics.ListAPIView):
    serializer_class = serializers.ContactListSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = models.Contact.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = my_filter.ContactListFilter


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = models.User.objects.all()


class UserCreate(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
