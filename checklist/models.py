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

    LOW_DANGER = 0
    MIDDLE_DANGER = 1
    HIGH_DANGER = 2

    DISPLAY_METHOD_CHOICES = [
        (LOW_DANGER, _("Low Danger")),
        (MIDDLE_DANGER, _("Middle Danger")),
        (HIGH_DANGER, _("High Danger")),
    ]

    branch_store = models.ForeignKey(BranchStore, on_delete=models.PROTECT, verbose_name=_("Branch Store"), related_name="inspections")
    inspectors = models.ManyToManyField(User, verbose_name=_("Inspectors"))
    classification = models.SmallIntegerField(
        _("Display method"), choices=DISPLAY_METHOD_CHOICES
    )
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    

    class Meta:
        verbose_name = _("Inspection")
        verbose_name_plural = _("Inspections")

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

class CheckListTabItem(models.Model):

    TEXT = "text"
    SHORT_TEXT = "short-text"
    RADIO = "radio"
    SELECT = "select"
    SELECT_IMAGE = "select_image"
    CHECKBOX = "checkbox"
    INTEGER = "integer"
    FLOAT = "float"
    DATE = "date"

    QUESTION_TYPES = (
        (TEXT, _("text")),
        (RADIO, _("radio")),
        (SELECT, _("select")),
        (CHECKBOX, _("checkbox")),
        (SELECT_IMAGE, _("Select Image")),
        (INTEGER, _("integer")),
        (FLOAT, _("float")),
        (DATE, _("date")),
    )

    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(blank=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    tab = models.ForeignKey(CheckListTab, on_delete=models.SET_NULL, verbose_name=_("Tab"), blank=True, null=True, related_name="items")
    inspection = models.ForeignKey(Inspection, on_delete=models.SET_NULL, verbose_name=_("Inspection"), blank=True, null=True, related_name="items")
    type = models.CharField(_("Type"), max_length=100, choices=QUESTION_TYPES, default=TEXT)
    choices = models.TextField(_("Choices"), blank=True, null=True, help_text=CHOICES_HELP_TEXT)

    order = models.PositiveSmallIntegerField(_("Display order"), blank=True, null=True)
    comment = models.TextField(_("Comment"), blank=True, null=True)
    is_important = models.BooleanField(_("Is Important"), blank=True)
        
    class Meta:
        verbose_name = _("Checklist Item")
        verbose_name_plural = _("Checklist Items")
        ordering = ("order",)

    def save(self, *args, **kwargs):
        if self.type in [CheckListTabItem.RADIO, CheckListTabItem.SELECT, CheckListTabItem.CHECKBOX]:
            validate_choices(self.choices)
        super(CheckListTabItem, self).save(*args, **kwargs)
    
    def get_clean_choices(self):
        """ Return split and stripped list of choices with no null values. """
        if self.choices is None:
            return []
        choices_list = []
        for choice in self.choices.split(settings.CHOICES_SEPARATOR):
            choice = choice.strip()
            if choice:
                choices_list.append(choice)
        return choices_list

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

    def __init__(self, *args, **kwargs):
        try:
            question = CheckListTabItem.objects.get(pk=kwargs["checklistitem_id"])
        except KeyError:
            question = kwargs.get("chech_list_item")
        body = kwargs.get("body")
        if question and body:
            self.check_answer_body(question, body)
        super(Answer, self).__init__(*args, **kwargs)

    @property
    def values(self):
        if self.body is None:
            return [None]
        if len(self.body) < 3 or self.body[0:3] != "[u'":
            return [self.body]
        values = []
        raw_values = self.body.split("', u'")
        nb_values = len(raw_values)
        for i, value in enumerate(raw_values):
            if i == 0:
                value = value[3:]
            if i + 1 == nb_values:
                value = value[:-2]
            values.append(value)
        return values

    
    def check_answer_body(self, chech_list_item, body):
        if check_list_item.type in [CheckListTabItem.RADIO, CheckListTabItem.SELECT, CheckListTabItem.SELECT_MULTIPLE]:
            choices = check_list_item.get_clean_choices()
            if body:
                if body[0] == "[":
                    answers = []
                    for i, part in enumerate(body.split("'")):
                        if i % 2 == 1:
                            answers.append(part)
                else:
                    answers = [body]
            for answer in answers:
                if answer not in choices:
                    msg = "Impossible answer '{}'".format(body)
                    msg += " should be in {} ".format(choices)
                    raise ValidationError(msg)
    
    def __str__(self):
        return "{} to '{}' : '{}'".format(self.__class__.__name__, self.check_list_item, self.body)