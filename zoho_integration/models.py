from django.db import models
import accounts.models
from datetime import datetime
import pytz
from member_management.models import Person

class Contact(models.Model):
    MEMBERSHIP_STATUS_CHOICES = (
            ('Full', 'Full Membership'),
            ('Starving', 'Starving Hacker'),
    )
    contact_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=300)
    membership_status = models.CharField(max_length=300, choices=MEMBERSHIP_STATUS_CHOICES)
    modified_time = models.DateTimeField()
    membership_end_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(accounts.models.PS1User, null=True)

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return u"{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()


class ContactChange(models.Model):
    contact = models.ForeignKey(Contact)
    field = models.CharField(max_length=300)
    detected_on = models.DateTimeField()
    old_value = models.CharField(null=True, default="None", max_length=300)
    new_value = models.CharField(null=True, default="None", max_length=300)

    @staticmethod
    def log(contact, field, new_value):
        old_value = getattr(contact, field) 
        if( old_value != new_value):
            change = ContactChange(
                contact = contact,
                field = field, 
                detected_on = datetime.now(pytz.utc),
                old_value = old_value,
                new_value = new_value
            )
            setattr(contact, field, new_value)
            contact.save()
            change.save()

        
