from django import forms
from django.db.models import Q
from datetime import date
from dateutil.relativedelta import relativedelta
from ckeditor.widgets import CKEditorWidget
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Person, PayPal

class mailform(forms.Form):
    CHOICES = [('all_members','All Members'),('full_members','Full Members')]
    from_email = forms.EmailField(label='From')
    reply_to = forms.EmailField()
    recipients =  forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    subject = forms.CharField()
    content = forms.CharField(widget=CKEditorWidget())

class PersonForm(forms.ModelForm):
    class Meta:
        fields = ['first_name', 'last_name', 'email', 'birthday',
                'membership_status', 'membership_start_date', 'street_address',
                'unit_number', 'city', 'state', 'zip_code', 'country']
        widgets = {
                'membership_start_date': DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
                'birthday': DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False, "startDate":"1900"}),
        }
        model = Person

class IDCheckForm(forms.Form):
    board_member = forms.BooleanField(label="You are a board member.")
    government_issued = forms.BooleanField(label="The ID is government issued.")
    name_matches = forms.BooleanField()
    birthday_matches = forms.BooleanField(label='The D.O.B. on the ID matches our records.')
    over_18 = forms.BooleanField(label='The person is over 18 years of age.')
    preferred_email = forms.BooleanField(label="The email address is correct and is the person's preferred email address.")
    waiver = forms.BooleanField(label="The person has filled out a waiver.")

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        super(IDCheckForm, self).__init__(*args, **kwargs)
        self.cleaned_data = {}

        pre_clean_fields = ['over_18', 'birthday_matches', 'preferred_email']
        for pre_clean_field in pre_clean_fields:
            self._pre_clean(pre_clean_field)
        self.fields['name_matches'].label = 'The name on the ID is {} {}'.format(self.person.first_name, self.person.last_name)
        #self.fields['waiver'].help_text = 'Have you filled out and signed a waiver?'

    def _pre_clean(self, name):
        """runs a validation step before the user has filled out the form.
        Useful for things like checking age and that data has been entered in already.
        """
        try:
            getattr(self, 'clean_{}'.format(name))()
        except forms.ValidationError as e:
            self.add_error(name, e)

    def clean_over_18(self):
        if not self.person.birthday:
            raise forms.ValidationError('No birthday entered for person')
        if self.person.birthday + relativedelta(years=18) > date.today():
            raise forms.ValidationError("Person is under 18 years of age, and is therefore not eligible for membership")

    def clean_birthday_matches(self):
        if self.person.birthday:
            self.fields['birthday_matches'].label = 'The D.O.B on the ID is {} ({})'.format(self.person.birthday.strftime('%B %d, %Y'), self.person.birthday.strftime('%m/%d/%y') )
            #self.fields['birthday_matches'].help_text = 'Is your birthday {}?'.format(self.person.birthday.strftime('%B %d, %Y'))
        else:
            raise forms.ValidationError('No birthday entered for person')

    def clean_preferred_email(self):
        if self.person.email:
            self.fields['preferred_email'].label = 'The Person\'s preferred email address is {}'.format(self.person.email)
            #self.fields['preferred_email'].help_text = 'Is your preferred email address {}?'.format(self.person.email)
        else:
            raise forms.ValidationError('No email address entered for person')

    def validate_id_checker(self):
        pass


class PayPalForm(forms.ModelForm):

    #same_as_personal_email = forms.BooleanField(required=False)
    email = forms.EmailField(required=False, label="PayPal Email")
    class Meta:
        fields = ['email']
        model = PayPal

class PersonSearchForm(forms.Form):
    """ My Poor mans's search function """
    membership_status = forms.ChoiceField(choices=(('','--'),) + Person.MEMBERSHIP_LEVEL, required=False)
    search = forms.CharField(label='Search', required=False)

    def get_queryset(self):
        search = self.cleaned_data['search']
        membership_status = self.cleaned_data['membership_status']
        if membership_status:
            queryset = Person.objects.filter(membership_status=membership_status)
        else:
            queryset = Person.objects.all()
        return queryset.filter(
            Q(first_name__icontains=search)|
            Q(last_name__icontains=search)|
            Q(email__icontains=search)|
            Q(paypal__email__icontains=search)
        )
