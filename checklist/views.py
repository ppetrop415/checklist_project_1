from django.shortcuts import render
from django.views.generic import ListView
from .models import Inspection, Response
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

    return render(request, 'checklist/dashboard.html', context)



class InspectionListView(ListView):
    model = Inspection
    template_name = "checklist/inspections.html"
    context_object_name = 'inspections'
    paginate_by = 10
    queryset = Response.objects.select_related('inspection').prefetch_related('inspectors')
    
    
