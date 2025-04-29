from django.shortcuts import render
from ..real_estate.models import Property

# Create your views here. 

def property_list(request):
    properties_data = Property.objects.all().order_by('created_at')
    print("Properties Data:", properties_data)
    
    print("Number of properties:", properties_data.count())  
    return render(request, 'index.html', {'properties': properties_data})

