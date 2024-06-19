import sys
from django.utils.timezone import now

try:
    from django.db import models
except Exception:
    print("There was an error loading Django modules. Do you have Django installed?")
    sys.exit()

from django.conf import settings
import uuid

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    WORK_RELATED = 'Work-Related'
    PERSONAL = 'Personal'
    HOME = 'Home'
    HEALTH_AND_FITNESS = 'Health & Fitness'
    FINANCE = 'Finance'
    SOCIAL = 'Social'
    EDUCATIONAL = 'Educational'
    ERRANDS = 'Errands'
    GOALS = 'Goals'
    MISCELLANEOUS = 'Miscellaneous'
    CATEGORY_CHOICES = [
        (WORK_RELATED , 'Work-Related'),
        (PERSONAL , 'Personal'),
        (HOME , 'Home'),
        (HEALTH_AND_FITNESS , 'Health & Fitness'),
        (FINANCE , 'Finance'),
        (SOCIAL , 'Social'),
        (EDUCATIONAL , 'Educational'),
        (ERRANDS , 'Errands'),
        (GOALS , 'Goals'),
        (MISCELLANEOUS, 'Miscellaneous'),
    ]
    name = models.CharField(
        null=False,
        max_length=30,
        choices=CATEGORY_CHOICES,
        default=MISCELLANEOUS
    )

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(null=False, max_length=30, default='online course')
    description = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(db_column='duedate')

    PENDING = 'Pending'
    COMPLETED = 'Completed'
    IN_PROGRESS = 'In Progress'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (IN_PROGRESS, 'In Progress')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'task'
