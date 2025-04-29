from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Client, Property, Inquiry, PropertyFeature, PropertyImage

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['user', 'user_id', 'phone_number', 'role']

class CustomPropertySerializer(ModelSerializer):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'city', 'state', 'property_type', 'status', 'seller']

class PropertyImageSerializer(ModelSerializer):

    def create(self, validated_data):
        property_id = self.context['property_id']
        return PropertyImage.objects.create(property_id=property_id, **validated_data)

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'caption']

class PropertySerializer(ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'address', 'city', 'state', 'zipcode', 'images', 'bedroom', 'bathroom', 'square_feet', 'lot_size', 'property_type', 'status', 'created_at', 'seller']


class InquirySerializer(ModelSerializer):

    class Meta:
        model = Inquiry
        fields = ['property', 'buyer', 'message', 'created_at']

        def create(self, validated_data):
            property_id = self.context['property_id']
            return Inquiry.objects.create(property_id=property_id, **validated_data)
        
class SimpleCustomPropertySerializer(ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'images', 'property_type', 'status', 'seller']

class PropertyFeatureSerializer(ModelSerializer):
    property = SimpleCustomPropertySerializer(read_only=True)
    class Meta:
        model = PropertyFeature
        fields = ['property']
