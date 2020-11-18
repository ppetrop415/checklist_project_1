import logging
import uuid

from django import forms
from django.conf import settings
from django.forms import models
from django.urls import reverse
from .models import Inspection, Answer, CheckListTabItem
from .signals import inspection_completed

LOGGER = logging.getLogger(__name__)

class InspectionForm(models.ModelForm):
    class Meta:
        model = Inspection
        fields = ()

    def __init__(self, *args, **kwargs):
        """ Expects a survey object to be passed in initially """
        self.activity = kwargs.pop("activity")
        self.inspectors = kwargs.pop("inspectors")
        self.branch_store = kwargs.pop("branch_store")


        super(InspectionForm, self).__init__(*args, **kwargs)
        self.uuid = uuid.uuid4().hex
        self.categories = self.activity.tabs
        
        self.inspection = False
        self.answers = False




    def add_questions(self, data):
        # add a field for each survey question, corresponding to the question
        # type as appropriate.

        for i, question in enumerate(self.survey.questions.all()):
            not_to_keep = i != self.step and self.step is not None

            self.add_question(question, data)
    



    def _get_preexisting_inspection(self):
        """Recover a pre-existing response in database.
        The user must be logged. Will store the response retrieved in an attribute
        to avoid multiple db calls.
        :rtype: Response or None"""
        if self.inspection:
            return self.inspection

        if not self.inspectors.is_authenticated:
            self.inspection = None
        else:
            try:
                self.inspection = Inspection.objects.select_related("branch_store").prefetch_related("activity").get(branch_store=self.branch_store, activity=self.activity)
            except Inspection.DoesNotExist:
                LOGGER.debug("No saved inspection for '%s' for user %s", self.activity, self.branch_store)
                self.inspection = None
        return self.inspection
    
    def _get_preexisting_answers(self):
        """Recover pre-existing answers in database.
        The user must be logged. A Response containing the Answer must exists.
        Will create an attribute containing the answers retrieved to avoid multiple
        db calls.
        :rtype: dict of Answer or None"""
        if self.answers:
            return self.answers
        inspection = self._get_preexisting_inspection()
        if inspection is None:
            self.answers = None
        try:
            answers = Answer.objects.filter(inspection=inspection).select_related("check_list_item")
            self.answers = {answer.check_list_item.id: answer for answer in answers.all()}
        except Answer.DoesNotExist:
            self.answers = None

        return self.answers

    def _get_preexisting_answer(self, check_list_item):
        """Recover a pre-existing answer in database.
        The user must be logged. A Response containing the Answer must exists.
        :param Question question: The question we want to recover in the
        response.
        :rtype: Answer or None"""
        answers = self._get_preexisting_answers()
        return answers.get(check_list_item.id, None)

    def get_question_initial(self, check_list_item, data):
        """Get the initial value that we should use in the Form
        :param Question question: The question
        :param dict data: Value from a POST request.
        :rtype: String or None"""
        initial = None
        answer = self._get_preexisting_answer(check_list_item)
        if answer:
            # Initialize the field with values from the database if any
            initial = answer.body
        if data:
            # Initialize the field field from a POST request, if any.
            # Replace values from the database
            initial = data.get("question_%d" % check_list_item.pk)
        return initial

    def add_question(self, check_list_item, data):
            """Add a question to the form.
            :param Question question: The question to add.
            :param dict data: The pre-existing values from a post request."""
            kwargs = {"label": check_list_item.text, "required": check_list_item.required}
            initial = self.get_question_initial(check_list_item, data)
            if initial:
                kwargs["initial"] = initial
            choices = self.get_question_choices(check_list_item)
            if choices:
                kwargs["choices"] = choices
            widget = self.get_question_widget(check_list_item)
            if widget:
                kwargs["widget"] = widget
            field = self.get_question_field(check_list_item, **kwargs)
            field.widget.attrs["category"] = check_list_item.check_list_tab.title if check_list_item.check_list_tab else ""

            # logging.debug("Field for %s : %s", question, field.__dict__)
            self.fields["check_list_item_%d" % check_list_item.pk] = field



    def save(self, commit=True):
        """ Save the response object """
        # Recover an existing response from the database if any
        #  There is only one response by logged user.
        inspection = self._get_preexisting_response()
        if inspection is not None:
            return None
        if inspection is None:
            inspection = super(InspectionForm, self).save(commit=False)
        inspection.activity = self.activity
        inspection.interview_uuid = self.uuid
        if self.user.is_authenticated:
            inspection.user = self.user
        inspection.save()
        # response "raw" data as dict (for signal)
        data = {"activity_id": inspection.activity.id, "interview_uuid": inspection.uuid, "responses": []}
        # create an answer object for each question and associate it with this
        # response.
        for field_name, field_value in list(self.cleaned_data.items()):
            if field_name.startswith("question_"):
                # warning: this way of extracting the id is very fragile and
                # entirely dependent on the way the question_id is encoded in
                # the field name in the __init__ method of this form class.
                item_id = int(field_name.split("_")[1])
                check_list_item = CheckListTabItem.objects.get(pk=item_id)
                answer = self._get_preexisting_answer(check_list_item)
                if answer is None:
                    answer = Answer(check_list_item=check_list_item)

                
                answer.body = field_value
                data["responses"].append((answer.check_list_item.id, answer.body))
                LOGGER.debug("Creating answer for question %d : %s", item_id, answer.check_list_item.type, field_value)
                answer.response = inspection
                answer.save()
        inspection_completed.send(sender=Inspection, instance=inspection, data=data)
        return inspection

