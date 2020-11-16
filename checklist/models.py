import uuid
import logging

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from business.models import Activity, BranchStore
from regions.models import CommonFields

LOGGER = logging.getLogger(__name__)

# Create your models here.
class Choice(models.Model):
    number = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')

    def __str__(self):
        return str(self.number)

class CheckListTab(CommonFields):
    activity = models.ManyToManyField(Activity)
    order = models.PositiveSmallIntegerField(_("Display order"))
    
    class Meta(CommonFields.Meta):
        verbose_name = _("Checklist Tab")
        verbose_name_plural = _("Checklist Tabs")
        ordering = ['order']
    
    def get_sorted_items(self):
        return self.items.all().order_by('order')

class CheckListTabItem(CommonFields):
    tab = models.ForeignKey(CheckListTab, on_delete=models.PROTECT, verbose_name=_("Tab"), related_name="items")
    choices = models.ManyToManyField(Choice)
    description = models.TextField(_("Description")) 
    comment = models.TextField(_("Comment"), blank=True, null=True)
    is_important = models.BooleanField(_("Is Important"), blank=True)
    order = models.PositiveSmallIntegerField(_("Display order"))
        
    class Meta:
        verbose_name = _("Checklist Item")
        verbose_name_plural = _("Checklist Items")
        ordering = ['order']

    def get_choices(self):
        return ", ".join([str(p) for p in self.choices.all()])

class Inspection(models.Model):

    LOW_DANGER = 'low'
    MIDDLE_DANGER = 'middle'
    HIGH_DANGER = 'high'

    DISPLAY_METHOD_CHOICES = [
        (LOW_DANGER, _("Low Danger")),
        (MIDDLE_DANGER, _("Middle Danger")),
        (HIGH_DANGER, _("High Danger")),
    ]

    branch_store = models.ForeignKey(BranchStore, on_delete=models.PROTECT, verbose_name=_("Branch Store"), related_name="inspections")
    inspectors = models.ManyToManyField(User, verbose_name=_("Inspectors"))
    classification = models.CharField(_("Display method"), max_length=10, choices=DISPLAY_METHOD_CHOICES)
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    uuid = models.UUIDField(_("Inspection unique identifier"), default=uuid.uuid4, primary_key=True, editable=False)
    date_created = models.DateTimeField(_("Creation date"), auto_now_add=True)

    class Meta:
        verbose_name = _("Inspection")
        verbose_name_plural = _("Inspections")
        ordering = ("-date_created",)

    def __str__(self):
        return str(self.branch_store)

    def get_sorted_tabs(self):
        return self.tabs.all().order_by('order')
    
    def get_inspectors(self):
        return ", ".join([str(p) for p in self.inspectors.all()])






























# class Response(models.Model):

#     """
#     A Response object is a collection of questions and answers with a
#     unique interview uuid.
#     """

#     created = models.DateTimeField(_("Creation date"), auto_now_add=True)
#     inspection = models.ForeignKey(Inspection, on_delete=models.PROTECT, verbose_name=_("Inspection"), related_name="responses")
#     inspectors = models.ManyToManyField(User, verbose_name=_("Inspectors"))
#     inspection_uuid = models.UUIDField(_("Inspection unique identifier"), default=uuid.uuid4, primary_key=True, editable=False)

#     class Meta:
#         verbose_name = _("Set of answers to Inspection Checklist")
#         verbose_name_plural = _("Set of answers to Inspection Checklists")
#         ordering = ("created",)

#     def __str__(self):
#         msg = "Response to {} by {}".format(self.inspection, self.inspectors)
#         msg += " on {} with {}".format(self.created, self.inspection_uuid)
#         return msg

#     def get_inspectors(self):
#         return ", ".join([str(p) for p in self.inspectors.all()])

#     def get_response_dict(self):
#         response_dict = dict()
#         for answer in self.answers.all():
#             response_dict[answer.checklistitem_id] = answer.body
#         return response_dict

# class Answer(models.Model):
#     check_list_item = models.ForeignKey(CheckListTabItem, on_delete=models.CASCADE, verbose_name=_("Checklist Item"), related_name="answers")
#     response = models.ForeignKey(Response, on_delete=models.CASCADE, verbose_name=_("Response"), related_name="answers")
#     created = models.DateTimeField(_("Creation date"), auto_now_add=True)
#     body = models.TextField(_("Choice"), blank=True, null=True)

#     def __str__(self):
#         return "{} to '{}' : '{}'".format(self.__class__.__name__, self.check_list_item, self.body)