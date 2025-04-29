from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import ClientSerializer, InquirySerializer, PropertyFeatureSerializer, CustomPropertySerializer, PropertySerializer, PropertyImageSerializer
from .models import Client, Property, Inquiry, PropertyImage, PropertyFeature
from .filters import PropertyFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly

# Create your views here.
class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (client, created) = Client.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ClientSerializer(client, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.prefetch_related('images').all()
    serializer_class = PropertySerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['goal_amount', 'created_at']

class PropertyImageviewSet(ModelViewSet):
    serializer_class = PropertyImageSerializer

    def get_serializer_context(self):
        return {'property_id': self.kwargs['property_pk']}

    def get_queryset(self):
        return PropertyImage.objects.filter(property_id=self.kwargs['property_pk'])
    
class PropertyFeatureViewSet(ModelViewSet):
    queryset = PropertyFeature.objects.all()
    serializer_class = PropertyFeatureSerializer


class InquiryViewSet(ModelViewSet):
    serializer_class = InquirySerializer

    def get_queryset(self):
        return Inquiry.objects.filter(property_id=self.kwargs['property_pk'])
    
    def get_serializer_context(self):
        return {'property_id': self.kwargs['property_pk']}
    