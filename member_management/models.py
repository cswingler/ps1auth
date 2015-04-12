from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template import Context, Template
from datetime import date
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import os
from smtplib import SMTPException
from ckeditor.fields import RichTextField
import re
from html2text import html2text
from bs4 import BeautifulSoup
from ps1auth.celery import app
from celery.contrib.methods import task_method
from accounts.models import PS1User
import reversion
from django.core.urlresolvers import reverse

class PersonManager(models.Manager):

    def full_members(self):
        return self.get_queryset().filter(membership_status='full_member')

    def starving_hackers(self):
        return self.get_queryset().filter(membership_status='starving_hacker')

    def members(self):
        return self.get_queryset().filter(Q(membership_status='full_member')|Q(membership_status='starving_hacker'))

@reversion.register
class Person(models.Model):
    MEMBERSHIP_LEVEL = (
            ('discontinued', 'Discontinued'),
            ('starving_hacker', 'Starving Hacker'),
            ('full_member', 'Full Member'),
            ('suspended', 'Suspended'),
            ('banned', 'Banned'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    membership_status = models.CharField(max_length=128, choices=MEMBERSHIP_LEVEL, default='discontinued')
    membership_start_date = models.DateField(default=date.today)
    street_address = models.CharField(max_length=128, blank=True, null=True)
    unit_number = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    zip_code = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = PersonManager()

    def __str__(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return u"{} {}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('member_management.views.person_detail', kwargs={'person_id':self.id})

    class Meta:
        verbose_name_plural = "people"

@reversion.register
class IDCheck(models.Model):
    person = models.ForeignKey('Person')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="Only Board Members are able to perform ID checks.")
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "ID Check for {} performed by {}".format(self.person, self.user)

class CRMPaymentMethod(models.Model):
    person = models.OneToOneField('Person', null=True)
    class Meta:
        abstract = True

class PayPal(CRMPaymentMethod):
    email = models.EmailField()
    paid_up_until = models.DateField(blank=True, null=True)
    class Meta:
        verbose_name = 'PayPal'
        verbose_name_plural = 'PayPal'

class Cash(CRMPaymentMethod):
    paid_up_until = models.DateField(blank=True)
    class Meta:
        verbose_name = 'cash'
        verbose_name_plural = 'cash'

@reversion.register
class Note(models.Model):
    person = models.ForeignKey('Person')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class EmailRecordManager(models.Manager):

    def send_email(self, user, from_email, reply_to_email, to_person, subject, html_content = None, text_content = None, attachments = []):
        """
        @param attachments a list of MIMEBase objects
        """
        total_emails_sent  = 0
        total_emails_failed = 0
        to_email = "{} {} <{}>".format(to_person.first_name, to_person.last_name, to_person.email)
        headers = {}
        if reply_to_email:
            headers['Reply-To'] = reply_to_email
        email_message = EmailMultiAlternatives(subject, text_content, from_email, [to_email], headers=headers)
        if html_content:
            email_message.attach_alternative(html_content, "text/html")
            email_message.mixed_subtype = 'related'

        # attachements
        for attachment in attachments:
            email_message.attach(attachment)

        # Record the email
        email_record = EmailRecord(
            subject=subject,
            message = email_message.message(),
            from_email = from_email,
            to_email = to_person.email,
            recipient = to_person,
            sender = user,
        )
        email_record.save()

        # Send
        try:
            email_message.send(fail_silently=False)
            email_record.status = 'sent'
            email_record.save()
            total_emails_sent += 1
        except SMTPException:
            email_record.statis = 'failed'
            email_record.save()
            total_emails_failed += 1
        return total_emails_sent

class EmailRecord(models.Model):
    subject = models.CharField(max_length=128)
    message = models.TextField()
    from_email = models.EmailField()
    reply_to_email = models.EmailField(blank=True)
    to_email = models.EmailField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    recipient = models.ForeignKey('Person')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = EmailRecordManager()
    status = models.CharField(default='pending', max_length=30)

    class Meta:
        ordering = ['-created_at']

class EmailTemplateManager(models.Manager):

    def individual_recipient(self):
        return self.filter(recipients='individual')

@reversion.register
class EmailTemplate(models.Model):
    RECIPIENTS = (
            ('all_members', 'All Members'),
            ('full_members', 'Full Members'),
            ('individual', 'Individual'),
    )
    from_name = models.CharField(max_length=255, blank=True)
    from_email = models.EmailField(verbose_name = 'From')
    reply_to_name = models.CharField(max_length=255, blank=True)
    reply_to_email = models.EmailField(verbose_name = 'Reply-To', blank=True)
    recipients = models.CharField(max_length=128, choices=RECIPIENTS, default='full_members')
    subject = models.CharField(max_length=128)
    message = RichTextField()
    objects = EmailTemplateManager()

    def __str__(self):
        return u'{}'.format(self.subject)

    def _convert_inline_images(self, html_content):
        soup = BeautifulSoup(html_content)
        attachments = []
        for tag in soup.find_all("img", src=re.compile("^{}".format(settings.MEDIA_URL))):
            basename = os.path.basename(tag['src'])
            #slice media_url off
            m = re.match("^{}(.*)".format(settings.MEDIA_URL), tag['src'])
            relative_file = m.group(1)
            #append file path to MEDIA_ROOT
            absolute_file = os.path.join(settings.MEDIA_ROOT, relative_file)
            image_file = open(absolute_file, 'rb')
            image = MIMEImage(image_file.read())
            image_file.close()
            image.add_header('Content-ID', "<{}>".format(basename))
            attachments.append(image)
            # rewrite tag in src
            tag['src'] = "cid:{}".format(basename)
        return (str(soup), attachments)

    def _send(self, user, target, extra_context):
        extra_context['recipient'] = target
        t = Template(self.message)
        message = t.render(Context(extra_context))
        html_content, attachments = self._convert_inline_images(message)
        txt_content = html2text(html_content)
        for attachment in self.attachments.all():
            file_data = MIMEApplication(attachment.file.read())
            file_data.add_header('Content-Disposition', 'attachment', filename=attachment.name)
            attachments.append(file_data)

        # Setup From email string.
        if(self.from_name):
            from_email = "{} <{}>".format(self.from_name, self.from_email)
        else:
            from_email = self.from_email

        reply_to_email= None
        if self.reply_to_email:
            if self.reply_to_name:
                reply_to_email = "{} <{}>".format(self.reply_to_name, self.reply_to_email)
            else:
                reply_to_email = self.reply_to_email

        return EmailRecord.objects.send_email(user, from_email, reply_to_email, target, self.subject, html_content, txt_content, attachments);

    def send(self, user, target = None, extra_context = {}):
        total = 0
        if target:
            send_email.delay(self.pk, user.pk, target.pk, extra_context)
            total += 1
        elif self.recipients == 'all_members':
            for member in Person.objects.members():
                send_email.delay(self.pk, user.pk, member.pk, extra_context)
                total += 1
        elif self.recipients == 'full_members':
            for member in Person.objects.full_members():
                send_email.delay(self.pk, user.pk, member.pk, extra_context)
                total += 1
        return total

@app.task    
def send_email(email_template_id, user_id, target_id, extra_context):
    email_template = EmailTemplate.objects.get(pk=email_template_id)
    user = PS1User.objects.get(pk=user_id)
    target = Person.objects.get(pk=target_id)
    email_template._send(user, target, extra_context)

class EmailAttachement(models.Model):
    name = models.CharField(max_length=255)
    email = models.ForeignKey('EmailTemplate', related_name='attachments')
    file = models.FileField(upload_to="attachements/%Y/%m/%d")

