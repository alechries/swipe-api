from . import models
from rest_framework import serializers


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Promotion
        fields = ('type', 'phrase', 'color')


class ApartmentListSerializer(serializers.ModelSerializer):
    promotion = PromotionSerializer()

    class Meta:
        model = models.Apartment
        fields = ('main_image', 'promotion', 'price', 'address', 'created_date', 'room_count', 'apartment_area')


class ApartmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apartment
        fields = ('main_image', 'price', 'address', 'adv_type', 'apartment_status', 'apartment_type', 'apart_class',
                  'apartment_area', 'kitchen_area', 'loggia', 'heating_type', 'settlement_type', 'commission',
                  'description', 'owner')


class FloorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Floor
        fields = ('section', 'name')


class FloorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Floor
        fields = ['id', 'section', 'name']

    def create(self, validated_data):
        return models.Floor.objects.create(**validated_data)
