from django.shortcuts import render
from .models import BranchStore

# Create your views here.
 

def branchstore(request):

    stores = BranchStore.objects.all()

    context = {
        'stores':stores
    }

    return render(request, 'business/stores.html', context) 