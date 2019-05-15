from django import forms
from django.utils.safestring import mark_safe

from .widgets import LanguageWidget


#
# Create account form
#

class CreateAccountForm(forms.Form):
    """
    This form is used to get data for a new **participant** account.
    Leaders should be made through the backend.

    Please note that these fields should have the same name as the arguments for
    RemoteApiUserManager.create_user(). The data from the form is directly
    passed through to that method through parameter unpacking.
    """

    MAILING_LIST_CHOICES = (
        (
            True,
            mark_safe(
                '<strong>wel</strong> mails ontvangen over nieuwe '
                'experimenten waar ik aan mee kan doen.'
            )
        ),
        (
            False,
            mark_safe(
                '<strong>geen</strong> mails ontvangen over nieuwe '
                'experimenten.'
            )
        ),
    )

    name = forms.Field(
        label="Voor- en achternaam"
    )

    email = forms.EmailField(
        label="Emailadres",
    )

    language = forms.Field(
        label="Mijn moedertaal is",
        widget=LanguageWidget,
    )

    #
    # The fields 'Multilingual' and 'Dyslexic' have a strange 'required'
    # config by design. To allow 'False' as a valid option, we need to
    # specify 'required=False'. However, this allows the field to accept no
    # answer (None) as a valid value, in which case the field will return
    # 'False'.
    # As this obviously is not what we want, we specify 'required' in the
    # widget 'attrs', so the HTML will still say the field is required,
    # prompting the user to pick the right answer for them.
    # Why this is the default behaviour of BooleanField is above me...
    #

    multilingual = forms.BooleanField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                (False, 'Eentalig'),
                (True, 'Meertalig (opgegroeid met meerdere moedertalen)'),
            ),
            attrs={
                'required': True,
            }
        ),
        required=False,
    )

    dyslexic = forms.BooleanField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                (True, 'Dyslectisch'),
                (False, 'Niet dyslectisch'),
            ),
            attrs={
                'required': True,
            }
        ),
        required=False,
    )

    mailing_list = forms.BooleanField(
        label='Ik wil',
        widget=forms.RadioSelect(
            choices=MAILING_LIST_CHOICES,
            attrs={
                'required': True,
            }
        ),
        required=False,
    )


#
# Mailing list form
#

class SubscribeToMailinglistForm(forms.Form):
    email = forms.EmailField(
        label="Emailadres",
    )

    language = forms.CharField(
        label="Mijn moedertaal is",
        widget=LanguageWidget,
    )

    mutlilingual = forms.CharField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                ('O', 'Eentalig'),
                ('M', 'Meertalig (opgegroeid met meerdere moedertalen)'),
            ),
        ),
    )

    dyslexic = forms.BooleanField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                (True, 'Dyslectisch'),
                (False, 'Niet dyslectisch'),
            ),
            attrs={
                'required': True,
            }
        ),
        required=False,
    )


#
# Register form
#

class BaseRegisterForm(forms.Form):
    name = forms.CharField(
        label="Naam"
    )

    email = forms.EmailField(
        label="Emailadres",
    )

    phone = forms.CharField(
        label="Telefoonnummer",
        widget=forms.TextInput(attrs={
            'type': 'tel'
        }),
    )

    birth_date = forms.DateField(
        label="Geboortedatum",
        widget=forms.DateInput(attrs={
            'type': 'date'
        }),
    )

    language = forms.CharField(
        label="Mijn moedertaal is",
        widget=LanguageWidget,
    )

    multilingual = forms.CharField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                ('N', 'Eentalig'),
                ('Y', 'Meertalig (opgegroeid met meerdere moedertalen)'),
            ),
        ),
    )

    sex = forms.CharField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                ('M', 'Man'),
                ('F', 'Vrouw'),
            ),
        ),
    )

    handedness = forms.CharField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                ('L', 'Linkshandig'),
                ('R', 'Rechtshandig'),
            ),
        ),
    )

    dyslexic = forms.CharField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                ('Y', 'Dyslectisch'),
                ('N', 'Niet dyslectisch'),
            ),
        )
    )

    social_status = forms.CharField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                ('S', 'Student'),
                ('O', 'Anders'),
            ),
        )
    )
