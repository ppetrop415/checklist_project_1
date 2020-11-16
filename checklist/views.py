# from django.shortcuts import render
# from django.views.generic import ListView, DetailView
# from .models import Inspection, Response, CheckListTab
# from business.models import Business

# # Create your views here.

# def home(request):

#     inspections = Inspection.objects.all()
#     total_inspections = inspections.count()
#     total_business = Business.objects.all().count()
#     high_danger = inspections.filter(classification=2).count()


#     context = {
#         'inspections':inspections,
#         'total_inspections':total_inspections,
#         'total_business':total_business,
#         'high_danger':high_danger
#     }

#     return render(request, 'checklist/dashboard.html', context)

# class InspectionListView(ListView):
#     model = Inspection
#     template_name = "checklist/inspections.html"
#     context_object_name = 'inspections'
#     paginate_by = 10
#     queryset = Inspection.objects.select_related("branch_store").prefetch_related('responses')

    
# class InspectionDetailView(DetailView):
#     model = Inspection
#     template_name = "checklist/inspection_detail.html"
#     context_object_name = 'inspection_detail'
#     # queryset = Inspection.objects.all().select_related('branch_store').prefetch_related('inspectors')
#     queryset = Inspection.objects.select_related('branch_store').prefetch_related('tabs', 'items', 'responses', 'inspectors')

# class CheckListTabListView(ListView):
#     model = CheckListTab
#     template_name = "checklist/tab_detail.html"
#     context_object_name = 'tabs'
#     queryset = CheckListTab.objects.prefetch_related('items')
