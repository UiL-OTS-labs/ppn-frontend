from django import forms
from django.utils.safestring import mark_safe

from .widgets import LanguageWidget, SexWidget


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

    def clean_email(self):
        data = self.cleaned_data.get('email')

        # Local import, as participants.utils imports this module. (We don't
        # want cycles!)
        from participant.utils import check_if_email_is_spammer
        if check_if_email_is_spammer(data):
            self.add_error(
                'email',
                'Dit emailadres staat bekend als een adres waarvandaan spam '
                'wordt verzonden, vul ajb een ander adres in.'
            )

        return data


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

    def clean_email(self):
        data = self.cleaned_data.get('email')

        # Local import, as participants.utils imports this module. (We don't
        # want cycles!)
        from participant.utils import check_if_email_is_spammer
        if check_if_email_is_spammer(data):
            self.add_error(
                'email',
                'Dit emailadres staat bekend als een adres waarvandaan spam '
                'wordt verzonden, vul ajb een ander adres in.'
            )

        return data



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
            'placeholder': 'dd-mm-yyyy',
            'pattern': '[0-9-]+',
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
        label='Mijn biologisch geslacht is',
        help_text='Waarom willen we je biologisch geslacht weten? '
                  'Geslachtshormonen zijn van invloed op de ontwikkeling en '
                  'het functioneren van de hersenen, en kunnen dus ook '
                  'invloed hebben op hoe de hersenen met taal omgaan. Het is '
                  'daarom gebruikelijk om op groepsniveau te rapporteren '
                  'hoeveel mannen en hoeveel vrouwen aan een studie hebben '
                  'deelgenomen. Soms worden de resultaten ook per groep '
                  'geanalyseerd.',
        widget=SexWidget
    )

    handedness = forms.CharField(
        label='Ik ben',
        help_text='Waarom willen we weten wat je dominante hand is? Links- '
                  'danwel rechtshandigheid gaat gepaard met verschillen in de '
                  'hersenen, die ook van invloed zouden kunnen zijn op hoe de '
                  'hersenen met taal omgaan. Het is daarom gebruikelijk om op '
                  'groepsniveau te rapporteren hoeveel links- en '
                  'rechtshandigen aan een studie hebben deelgenomen. Soms '
                  'worden de resultaten ook per groep geanalyseerd.',
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

    def clean_email(self):
        data = self.cleaned_data.get('email')

        # Local import, as participants.utils imports this module. (We don't
        # want cycles!)
        from participant.utils import check_if_email_is_spammer
        if check_if_email_is_spammer(data):
            self.add_error(
                'email',
                'Dit emailadres staat bekend als een adres waarvandaan spam '
                'wordt verzonden, vul ajb een ander adres in.'
            )

        return data
