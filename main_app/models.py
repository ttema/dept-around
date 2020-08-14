from django.db import models
from django.utils import timezone
from .choices import *


class Event(models.Model):
    """
    Модель события
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    creation_date = models.DateField(default=timezone.now)
    event_date = models.DateField(default=timezone.now)
    creator = models.CharField(max_length=50)
    uni_id = models.IntegerField(null=True)


class Payment(models.Model):
    """
    Модель платежа события
    """
    name = models.CharField(blank=True, max_length=50)
    description = models.CharField(blank=True, max_length=50)
    destination = models.CharField(blank=True, max_length=50)
    participants = models.CharField(max_length=200)
    creditor = models.CharField(max_length=20, default=' ')
    percents_type = models.IntegerField(choices=PERCENT_CHOICES, default=1)
    percents = models.IntegerField(default=0)
    total_loan_sum = models.FloatField(null=True)
    sum_with_percents = models.IntegerField(default=0)
    period = models.IntegerField(default=0)
    payment_date = models.DateField(default=timezone.now, blank=True)
    creator = models.CharField(max_length=20, default=' ', blank=True)
    creation_date = models.DateField(default=timezone.now)
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
