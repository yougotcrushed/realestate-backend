from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

rounter = DefaultRouter()
rounter.register('properties', views.PropertyViewSet, basename='property')
rounter.register('clients', views.ClientViewSet)
rounter.register('property_features', views.PropertyFeatureViewSet)

property_router = routers.NestedDefaultRouter(rounter, 'properties', lookup='property')
property_router.register('inquiries', views.InquiryViewSet, basename='property-inquiry')
property_router.register('images', views.PropertyImageviewSet, basename='property-image')

urlpatterns = rounter.urls + property_router.urls
