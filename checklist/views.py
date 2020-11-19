import logging
from django.shortcuts import redirect, render, reverse
from django.views.generic import ListView, DetailView, View, TemplateView
from .models import Inspection, CheckListTab
from business.models import Business
from .forms import InspectionForm

LOGGER = logging.getLogger(__name__)
# Create your views here.

def home(request):

    inspections = Inspection.objects.all()
    total_inspections = inspections.count()
    total_business = Business.objects.all().count()
    high_danger = inspections.filter(classification='high').count()

    context = {
        'inspections':inspections,
        'total_inspections':total_inspections,
        'total_business':total_business,
        'high_danger':high_danger
    }

    return render(request, 'checklist/dashboard.html', context)

class InspectionDetail(View):
    def get(self, request, *args, **kwargs):
        inspection = kwargs.get("inspection")
        form = InspectionForm(inspection=inspection)
        categories = form.current_categories()

        template_name = 'checklist/new_inspection_detail.html'

        context = {
            "inspection_form":form,
            "inspection":inspection,
            "categories":categories,
        }

        return render(request, template_name, context)
    
    def post(self, request, *args, **kwargs):
        inspection = kwargs.get("inspection")
        form = InspectionForm(request.POST, inspection=inspection)
        categories = form.current_categories()

        template_name = 'checklist/new_inspection_detail.html'

        context = {
            "inspection_form":form,
            "inspection":inspection,
            "categories":categories,
        }

        if form.is_valid():
            return self.treat_valid_form(form, kwargs, request, inspection)
        return self.handle_invalid_form(context, form, request, inspection)

    @staticmethod
    def handle_invalid_form(context, form, request, inspection):
        LOGGER.info("Non valid form: <%s>", form)
        template_name = "checklist/inspection_detail.html"
        return render(request, template_name, context)

    def treat_valid_form(self, form, kwargs, request, survey):
        session_key = "inspection_%s" % (kwargs["id"],)
        if session_key not in request.session:
            request.session[session_key] = {}
        for key, value in list(form.cleaned_data.items()):
            request.session[session_key][key] = value
            request.session.modified = True
            inspection = None
            inspection = form.save()
        if inspection is None:
            return redirect(reverse("survey-list"))
        del request.session[session_key]
        return redirect("inspection-confirmation", uuid=inspection.uuid)

class ConfirmInspectionView(TemplateView):
    template_name = "checklist/confirm.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmInspectionView, self).get_context_data(**kwargs)
        context["uuid"] = str(kwargs["uuid"])
        context["inspection"] = Inspection.objects.get(uuid=context["uuid"])
        return context

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

    
#     def get_context_data(self, **kwargs):
#         context = super(Inspection, self).get_context_data(**kwargs)
#         return context



# class CheckListTabListView(ListView):
#     model = CheckListTab
#     template_name = "checklist/tab_detail.html"
#     context_object_name = 'tabs'
#     queryset = CheckListTab.objects.prefetch_related('items')
