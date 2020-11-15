from django.urls import reverse 

from business.models import BranchStore

import uuid
import logging
from django.conf import settings
from django.contrib.auth.models import User
from business.models import Activity, TypeOfActivity
from django.core.exceptions import ValidationError
from django.db import models


from django.utils.translation import gettext_lazy as _


LOGGER = logging.getLogger(__name__)

# Create your models here.

CHOICES_HELP_TEXT = _(
    """
    The choices field is only used if the question type is 'radio', 'select', or 
    'select multiple' provide a comma-separated list of options for this question.
    """
)

def validate_choices(choices):
    """Verifies that there is at least two choices in choices
    :param String choices: The string representing the user choices.
    """
    values = choices.split(settings.CHOICES_SEPARATOR)
    empty = 0
    for value in values:
        if value.replace(" ", "") == "":
            empty += 1
    if len(values) < 2 + empty:
        msg = "The selected field requires an associated list of choices."
        msg += " Choices must contain more than one item."
        raise ValidationError(msg)

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
    classification = models.CharField(
        _("Display method"), max_length=10, choices=DISPLAY_METHOD_CHOICES
    )
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    

    class Meta:
        verbose_name = _("Inspection")
        verbose_name_plural = _("Inspections")
        ordering = ("-id",)

    def __str__(self):
        return str(self.branch_store)

    def get_sorted_tabs(self):
        return self.tabs.all().order_by('order')

    def eav_report_data(self):
        report_data = []
        inspectors = self.inspectors.order_by('full_name')
        tabs = self.tabs.get_sorted_tabs()
        items = self.items.get_sorted_items()
        for inspector in inspectors:
            inspector_data = [inspector.full_name]
            inspector_responses = inspector.get_response_dict()
            for tab in tabs:
                for item in items:
                    if item.id in inspector_responses:
                        inspector_data.append(inspector_responses[item.id])
                    else:
                        inspector_data.append(None)
                report_data.append(inspector_data)
            report_data.append(inspector_responses)
        return tabs, items, report_data
    
    def get_inspectors(self):
        return ", ".join([str(p) for p in self.inspectors.all()])
    
    def get_absolute_url(self):
        return reverse('inspection-detail', kwargs={'pk': self.pk})
    

class CheckListTab(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(blank=True)
    inspection = models.ForeignKey(Inspection, on_delete=models.SET_NULL, verbose_name=_("Inspection"), blank=True, null=True, related_name="tabs")
    activity = models.ManyToManyField(Activity)
    order = models.PositiveSmallIntegerField(_("Display order"), blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Checklist Tab")
        verbose_name_plural = _("Checklist Tabs")
        ordering = ("order",)

    def get_sorted_items(self):
        return self.items.all().order_by('order')

class Choise(models.Model):
    number = models.PositiveSmallIntegerField()
    """Model definition for Choise."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Choise."""

        verbose_name = 'Choise'
        verbose_name_plural = 'Choises'

    def __str__(self):
        """Unicode representation of Choise."""
        return str(self.number)

class CheckListTabItem(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(blank=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    tab = models.ForeignKey(CheckListTab, on_delete=models.SET_NULL, verbose_name=_("Tab"), blank=True, null=True, related_name="items")
    inspection = models.ForeignKey(Inspection, on_delete=models.SET_NULL, verbose_name=_("Inspection"), blank=True, null=True, related_name="items")
    # type = models.CharField(_("Type"), max_length=100, choices=QUESTION_TYPES, default=TEXT)
    # choices = models.TextField(_("Choices"), blank=True, null=True, help_text=CHOICES_HELP_TEXT)
    choices = models.ManyToManyField(Choise)
    order = models.PositiveSmallIntegerField(_("Display order"), blank=True, null=True)
    comment = models.TextField(_("Comment"), blank=True, null=True)
    is_important = models.BooleanField(_("Is Important"), blank=True)
        
    class Meta:
        verbose_name = _("Checklist Item")
        verbose_name_plural = _("Checklist Items")
        ordering = ("order",)
    
    def __str__(self):
        return self.title




class Response(models.Model):

    """
    A Response object is a collection of questions and answers with a
    unique interview uuid.
    """

    created = models.DateTimeField(_("Creation date"), auto_now_add=True)
    inspection = models.ForeignKey(Inspection, on_delete=models.PROTECT, verbose_name=_("Inspection"), related_name="responses")
    inspectors = models.ManyToManyField(User, verbose_name=_("Inspectors"))
    inspection_uuid = models.UUIDField(_("Inspection unique identifier"), default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name = _("Set of answers to Inspection Checklist")
        verbose_name_plural = _("Set of answers to Inspection Checklists")
        ordering = ("created",)

    def __str__(self):
        msg = "Response to {} by {}".format(self.inspection, self.inspectors)
        msg += " on {} with {}".format(self.created, self.inspection_uuid)
        return msg

    def get_inspectors(self):
        return ", ".join([str(p) for p in self.inspectors.all()])

    def get_response_dict(self):
        response_dict = dict()
        for answer in self.answers.all():
            response_dict[answer.checklistitem_id] = answer.body
        return response_dict

class Answer(models.Model):
    check_list_item = models.ForeignKey(CheckListTabItem, on_delete=models.CASCADE, verbose_name=_("Checklist Item"), related_name="answers")
    response = models.ForeignKey(Response, on_delete=models.CASCADE, verbose_name=_("Response"), related_name="answers")
    created = models.DateTimeField(_("Creation date"), auto_now_add=True)
    body = models.TextField(_("Choice"), blank=True, null=True)

    def __str__(self):
        return "{} to '{}' : '{}'".format(self.__class__.__name__, self.check_list_item, self.body)