from rest_framework import viewsets
from .serializers import CheckListTabItemSerializer, CheckListTabSerializer, ActivitySerializer, BranchStoreSerializer, BusinessStoreSerializer, AnswerSerializer, InspectionSerializer
from ..models import CheckListTabItem, CheckListTab, Answer, Inspection
from business.models import Activity, Business, BranchStore

class CheckListTabItemViewSet(viewsets.ModelViewSet):
    queryset = CheckListTabItem.objects.all()
    serializer_class = CheckListTabItemSerializer

class CheckListTabViewSet(viewsets.ModelViewSet):
    queryset = CheckListTab.objects.all()
    serializer_class = CheckListTabSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class BranchStoreViewSet(viewsets.ModelViewSet):
    queryset = BranchStore.objects.select_related('business', 'health_regulator', 'region', 'region_unity', 'state', 'zip_code', 'activity', 'type_of_activity')
    serializer_class = BranchStoreSerializer

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessStoreSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.select_related('branch_store').prefetch_related('answers')
    serializer_class = InspectionSerializer