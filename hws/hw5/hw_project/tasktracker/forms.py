
from datetime import date
from datetime import datetime

from django.forms import Form
from django.forms import ValidationError

from django.forms import CharField
from django.forms import DateField
from django.forms import ChoiceField
# from django.forms import RadioSelect

from django.forms.widgets import SelectDateWidget
from django.forms.widgets import RadioSelect

from .utils import TASK_STATES


class TaskForm(Form):

    title = CharField(max_length=100, min_length=3)
    estimate = DateField(widget=SelectDateWidget, initial=date.today())

    choices = [
        (TASK_STATES.in_progress, TASK_STATES.in_progress),
        (TASK_STATES.ready, TASK_STATES.ready),
    ]
    state = ChoiceField(choices=choices, widget=RadioSelect)


class AddTaskForm(TaskForm):

    def clean_estimate(self):

        est = self.cleaned_data['estimate']
        today = date.today()

        if est < today:
            raise ValidationError("Minimum value equal today!")

        return est
