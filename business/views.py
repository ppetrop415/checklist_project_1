from django.shortcuts import render
from .models import BranchStore, Activity
from django.views.generic import ListView, DetailView

# Create your views here.
 


class BranchStoreListView(ListView):
    model = BranchStore
    template_name = "business/stores.html"
    context_object_name = 'stores'
    paginate_by = 10


class BranchStoreDetailView(DetailView):
    model = BranchStore
    template_name = "TEMPLATE_NAME"


class ActivityListView(ListView):
    model = Activity
    template_name = "business/activities.html"
    context_object_name = 'activities'

class ActivityDetailView(DetailView):
    model = Activity
    template_name = "business/activity_detail.html"
    context_object_name = 'activity'


# def branchstore(request):
    
#     stores = BranchStore.objects.all()

#     context = {
#         'stores':stores
#     }

#     return render(request, 'business/stores.html', context) 