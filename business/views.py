from django.shortcuts import render
from .models import BranchStore
from django.views.generic import ListView

# Create your views here.
 


class BranchStoreListView(ListView):
    model = BranchStore
    template_name = "business/stores.html"
    context_object_name = 'stores'




# def branchstore(request):
    
#     stores = BranchStore.objects.all()

#     context = {
#         'stores':stores
#     }

#     return render(request, 'business/stores.html', context) 