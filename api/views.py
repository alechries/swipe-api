from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from . import models
from datetime import datetime
from django.db.models import Q
from itertools import chain
from . import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from . import filters as my_filter
from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter


def auth(request):
    return render(request, 'oauth.html')


class ApartmentList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ApartmentListSerializer
    queryset = models.Apartment.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = my_filter.ApartmentFilter


class ApartmentDetail(generics.RetrieveAPIView):
    serializer_class = serializers.ApartmentDetailSerializer
    queryset = models.Apartment.objects.all()


class FloorCreate(generics.CreateAPIView):
    serializer_class = serializers.FloorCreateSerializer


class FloorList(generics.ListAPIView):
    serializer_class = serializers.ApartmentListSerializer
    queryset = models.Floor.objects.all()