from django.contrib import admin
from .models import Activity, TypeOfActivity, CheckListTab
# Register your models here.


admin.site.register(Activity)
admin.site.register(TypeOfActivity)
admin.site.register(CheckListTab)