from django.shortcuts import render
from .models import Inspection
from business.models import Business

# Create your views here.

def home(request):

    inspections = Inspection.objects.all()
    total_inspections = inspections.count()
    total_business = Business.objects.all().count()
    high_danger = inspections.filter(classification=2).count()


    context = {
        'inspections':inspections,
        'total_inspections':total_inspections,
        'total_business':total_business,
        'high_danger':high_danger
    }

    return render(request, 'home.html', context)
