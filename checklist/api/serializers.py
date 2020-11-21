from rest_framework import serializers

from ..models import Choice, CheckListTab, CheckListTabItem, Answer, Inspection
from business.models import Activity, Business, BranchStore

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'number']

class CheckListTabItemSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = CheckListTabItem
        fields = ['id', 'order', 'title', 'slug', 'choices', 'description', 'comment', 'is_important']

class CheckListTabSerializer(serializers.ModelSerializer):

    items = CheckListTabItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = CheckListTab
        fields = ['id', 'order', 'title', 'slug', 'items']

class ActivitySerializer(serializers.ModelSerializer):

    tabs = CheckListTabSerializer(many=True, read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'url','order', 'title', 'slug', 'tabs']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

class BranchStoreSerializer(serializers.ModelSerializer):
    
    region_unity = serializers.StringRelatedField()
    region = serializers.StringRelatedField()
    state = serializers.StringRelatedField()
    zip_code = serializers.StringRelatedField()
    business = serializers.StringRelatedField()
    activity = serializers.StringRelatedField()
    type_of_activity = serializers.StringRelatedField()
    health_regulator = serializers.StringRelatedField()
    
    class Meta:
        model = BranchStore
        fields = ['id', 'url','business', 'title', 'slug', 'health_regulator', 'notify_number', 'region', 'region_unity', 'state', 'zip_code', 'address', 'address_number', 'email', 'activity', 'type_of_activity']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

class BusinessStoreSerializer(serializers.ModelSerializer):

    branchstores = BranchStoreSerializer(many=True, read_only=True)

    class Meta:
        model = Business
        fields = ['id', 'url','title', 'slug', 'owner', 'vat', 'branchstores']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

class AnswerSerializer(serializers.ModelSerializer):


    class Meta:
        model = Answer
        fields = '__all__'

class InspectionSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Inspection
        fields = ['branch_store', 'inspectors', 'classification', 'score', 'uuid', 'date_created', 'answers']