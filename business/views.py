# from django.shortcuts import render
from .models import BranchStore, Activity
from django.views.generic import ListView, DetailView, View
from checklist.models import CheckListTab, CheckListTabItem, Activity
# Create your views here.
 


# class BranchStoreListView(ListView):
#     model = BranchStore
#     template_name = "business/stores.html"
#     context_object_name = 'stores'
#     paginate_by = 10


# class BranchStoreDetailView(DetailView):
#     model = BranchStore
#     template_name = "TEMPLATE_NAME"



class ActivityListView(ListView):
    model = Activity
    template_name = "business/activities.html"
    context_object_name = 'activities'

class ActivityDetailView(DetailView):
    model = Activity
    template_name = "business/activity_detail.html"
    context_object_name = 'activity_detail'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = Activity.objects.prefetch_related('checklisttab_set').prefetch_related('checklisttab_set__items')
        return context
    
    