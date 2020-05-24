from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    # Django provides numerous places where you can validate your data. The easiest way to validate a single field is to override the method clean_<fieldname>() for the field you want to check. So for example, we can validate that entered renewal_date values are between now and 4 weeks by implementing clean_renewal_date() as shown below.
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # CHeck if a date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid Date - renewal in past'))
        
        # Check if a date is in the allowed range(+4 weeks from today)
        if data > datetime.date.today() +datetime.timedelta(weeks=4):
            raise ValidationError(_("invalid Date - Renwal more than 4 weeks ahead"))

        return data

# A basic ModelForm containing the same field as our original RenewBookForm is shown below. All you need to do to create the form is add class Meta with the associated model (BookInstance) and a list of the model fields to include in the form (you can include all fields using fields = '__all__', or you can use exclude (instead of fields) to specify the fields not to include from the model).

""" from django.forms import ModelForm
from catalog.models import BookInstance

class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
         data = self.cleaned_data['due_back']

          Check if a date is not in the past.
         if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

         Check if a date is in the allowed range (+4 weeks from today).
         if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
         return data

     class Meta:
         model = BookInstance
         fields = ['due_back']
         labels = {'due_back': _('Renewal Date')}
         help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')} """

# The class RenewBookModelForm above is now functionally equivalent to our original RenewBookForm. You could import and use it wherever you currently use RenewBookForm as long as you also update the corresponding form variable name from renewal_date to due_back as in the second form declaration: RenewBookModelForm(initial={'due_back': proposed_renewal_date}.