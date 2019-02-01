from django import forms

from .widgets import LanguageWidget


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

    dyslexic = forms.CharField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=(
                ('D', 'Dyslectisch'),
                ('ND', 'Niet dyslectisch'),
            ),
        )
    )


class BaseRegisterForm(forms.Form):

    name = forms.CharField(
        label="Naam"
    )

    email = forms.EmailField(
        label="Emailadres",
    )

    phone = forms.CharField(
        label="Telefoonnummer",
        widget=forms.TextInput(attrs={'type':'tel'}),
    )

    birth_date = forms.DateField(
        label="Geboortedatum",
        widget=forms.DateInput(attrs={'type':'date'}),
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
                ('D', 'Dyslectisch'),
                ('ND', 'Niet dyslectisch'),
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
