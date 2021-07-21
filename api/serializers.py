from . import models
from rest_framework import serializers


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Promotion
        fields = ('type', 'phrase', 'color')


class ApartmentListSerializer(serializers.ModelSerializer):
    promotion = PromotionSerializer()

    class Meta:
        model = models.Apartment
        fields = ('id', 'main_image', 'promotion', 'price', 'address', 'created_date', 'room_count', 'apartment_area',
                  'promotion', 'house', 'floor')


class ApartmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apartment
        fields = ('id', 'main_image', 'price', 'address', 'adv_type', 'apartment_status', 'apartment_type', 'apart_class',
                  'apartment_area', 'kitchen_area', 'loggia', 'heating_type', 'settlement_type', 'commission',
                  'description', 'owner', 'promotion')


class ApartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apartment
        fields = ['address', 'floor', 'price', 'document', 'apartment_type', 'room_count', 'apart_class',
                  'apartment_status', 'apartment_area', 'kitchen_area', 'loggia', 'heating_type', 'commission',
                  'description', 'owner']

    def create(self, validated_data):
        return models.Apartment.objects.create(**validated_data)



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


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = ['id', 'user', 'first_name', 'last_name']


class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'subscribe_expired', 'subscribe', 'agent_first_name',
                  'agent_last_name', 'notification']


class HouseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.House
        fields = ['id', 'address']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'


class HouseDetailSerializer(serializers.ModelSerializer):
    manager = ContactSerializer()

    class Meta:
        model = models.House
        fields = '__all__'



