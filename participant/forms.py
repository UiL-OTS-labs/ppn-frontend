from django import forms

from .widgets import LanguageWidget


class BaseRegisterForm(forms.Form):

    name = forms.CharField(
        label="Naam"
    )

    email = forms.EmailField(
        label="Emailadres",
    )

    phone = forms.CharField(
        label="Telefoonnummer",
    )

    birth_date = forms.DateField(
        label="Geboortedatum",
    )

    language = forms.CharField(
        label="Mijn moedertaal is",
        widget=LanguageWidget,
    )

    mutlilingual = forms.BooleanField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                (False, 'Eentalig'),
                (True, 'Meertalig (opgegroeid met meerdere moedertalen)'),
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

    dyslexic = forms.BooleanField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                (True, 'Dyslectisch'),
                (False, 'Niet dyslectisch'),
            ),
        )
    )

    social_status = forms.CharField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                ('D', 'Student'),
                ('O', 'Anders'),
            ),
        )
    )