from django.db import models, transaction
from django.conf import settings
from datetime import datetime
from django.utils import timezone
import reversion

class MemberPointManager(models.Manager):
    use_for_related_fields = True
    
    def valid(self):
        now = timezone.now()
        last_year = now.replace(now.year -1)
        return self.get_queryset().filter(created_on__gte=last_year).filter(consumed_on=None)

    def consumed(self):
        return self.get_queryset().filter(consumed_on__isnull=False)

    def expired(self):
        now = timezone.now()
        last_year = now.replace(now.year -1)
        return self.get_queryset().filter(created_on__lt=last_year)

    def next_to_expire(self):
        return self.valid().order_by('created_on').first()

@reversion.register
class MemberPoint(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    reason = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    consumed_on = models.DateTimeField(null=True, blank=True)
    objects = MemberPointManager()

    def __str__(self):
        return u'MemberPoint({}, {}, {}, {})'.format(
            self.owner,
            self.reason,
            self.created_on,
            self.consumed_on,
        )

    def consume(self):
        with transaction.atomic(), reversion.create_revision():
            self.consumed_on = timezone.now()
            self.save()

    def expiration_date(self):
        return self.created_on.replace(year = self.created_on.year + 1)

    def is_expired(self):
        now = timezone.now()
        return not self.consumed_on and now.replace(now.year-1) > self.created_on 

