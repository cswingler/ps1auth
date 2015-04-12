from django.db import models
from member_management.models import Person

class Token(models.Model):
    token = models.CharField(max_length=36)
    person = models.ForeignKey(Person)
