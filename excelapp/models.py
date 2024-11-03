from django.db import models
from django_jalali.db import models as jmodels

class Event(models.Model):
    start_date = jmodels.jDateField()
    end_date = jmodels.jDateField()


