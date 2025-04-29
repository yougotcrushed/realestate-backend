from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from .models import Property, Inquiry, PropertyFeature, PropertyImage, Feature, Client

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user__first_name', 'user__last_name', 'phone_number', 'role']
    list_editable = ['role']
    list_select_related = ['user']
    ordering  = ['user__first_name', 'user__last_name']
    list_per_page = 10
    search_fields = ['User__first_name__istartswith', 'User__last_name__istartswith']

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    readonly_fields = ['thumbnail']
    fields = ['image', 'caption', 'thumbnail']
    extra = 1

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f"<img src='{instance.image.url}' class='thumbnail' />")
        return ''

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ['title', 'price', 'property_type', 'status']
    list_editable = ['status']
    list_select_related = ['seller']
    list_per_page = 10
    ordering  = ['title', 'price']
    search_fields = ['title__istartswith']

    class Media:
        css = {
            'all': ['real_estate/styles.css']
        }

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['property', 'buyer', 'created_at']
    list_select_related = ['property', 'buyer']
    list_per_page = 10

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering  = ['name']
    list_per_page = 10
    search_fields = ['name__istartswith']

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'image', 'thumbnail']
    ordering  = ['property']
    readonly_fields = ['thumbnail']
    list_select_related = ['property']
    list_per_page = 10

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f"<img src='{instance.image.url}' class='thumbnail' />")
        return ''

    class Media:
        css = {
            'all': ['real_estate/styles.css']
        }

@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ['property', 'feature']
    ordering  = ['property']
    list_select_related = ['property', 'feature']
    list_per_page = 10

