from django.db import models

from team.models import Team
from django.contrib.auth import get_user_model
import datetime

# Create your models here.
class Session(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title

class Class(Session):
    DAYS_OF_WEEK = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    
    class Meta:
        constraints = [
            # models.CheckConstraint(
            #     check=models.Q(start_time__lt=models.F('end_time')),
            #     name = 'starts_before_end'
            # )
        ]
    
    def __str__(self):
        return self.title

    def get_length(self):
        date = datetime.date(1,1,1)
        datetime1 = datetime.datetime.combine(date, self.start_time)
        datetime2 = datetime.datetime.combine(date, self.end_time)
        return (datetime2 - datetime1).seconds // 60

    def in_minutes(self):
        return self.start_time.hour * 60 + self.start_time.minute

class Notice(Session):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Event(Session):
    start = models.DateTimeField()
    end = models.DateTimeField()
    def __str__(self):
        return self.title

class Feedback(models.Model):
    eventid = models.IntegerField()
    teamid = models.CharField(max_length=20)
    feedback = models.CharField(max_length=20)
    score = models.IntegerField()
