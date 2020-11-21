from rest_framework import viewsets
from .serializers import CheckListTabItemSerializer, CheckListTabSerializer, ActivitySerializer, BranchStoreSerializer, BusinessStoreSerializer, AnswerSerializer, InspectionSerializer
from ..models import CheckListTabItem, CheckListTab, Answer, Inspection
from business.models import Activity, Business, BranchStore

class CheckListTabItemViewSet(viewsets.ModelViewSet):
    queryset = CheckListTabItem.objects.prefetch_related('choices')
    serializer_class = CheckListTabItemSerializer

class CheckListTabViewSet(viewsets.ModelViewSet):
    queryset = CheckListTab.objects.all()
    serializer_class = CheckListTabSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.prefetch_related('tabs')
    serializer_class = ActivitySerializer
    lookup_field = 'slug'

class BranchStoreViewSet(viewsets.ModelViewSet):
    queryset = BranchStore.objects.select_related('business', 'health_regulator', 'region', 'region_unity', 'state', 'zip_code', 'activity', 'type_of_activity')
    serializer_class = BranchStoreSerializer
    lookup_field = 'slug'

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessStoreSerializer
    lookup_field = 'slug'

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.select_related('branch_store').prefetch_related('answers')
    serializer_class = InspectionSerializer