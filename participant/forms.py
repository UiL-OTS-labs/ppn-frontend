from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from .widgets import LanguageWidget, SexWidget


#
# Sign up form
#

class SignUpForm(forms.Form):

    ACCOUNT_CHOICES = (
        (
            True,
            "Ja, ik wil een account aanmaken"
        ),
        (
            False,
            "Nee, ik wil geen account aanmaken"
        ),
    )

    MULTILINGUAL_CHOICES = (
        (
            False,
            'Eentalig'
        ),
        (
            True,
            'Meertalig (opgegroeid met meerdere moedertalen)'
        ),
    )

    MAILING_LIST_CHOICES = (
        (
            True,
            "Ja, ik wil graag bericht krijgen over nieuwe experimenten"
        ),
        (
            False,
            "Nee, ik wil geen bericht krijgen over nieuwe experimenten"
        ),
    )

    name = forms.Field(
        label="Voor- en achternaam",
        required=False,
    )

    email = forms.EmailField(
        label="Emailadres",
    )

    language = forms.CharField(
        label="Mijn moedertaal is",
        widget=LanguageWidget,
    )

    #
    # The following BooleanFields have a strange 'required' config by design.
    # To allow 'False' as a valid option, we need to specify
    # 'required=False'. However, this allows the field to accept no  answer
    # (None) as a valid value, in which case the field will return 'False'.
    # As this obviously is not what we want, we specify 'required' in the
    # widget 'attrs', so the HTML will still say the field is required,
    # prompting the user to pick the right answer for them.
    # Why this is the default behaviour of BooleanField is above me...
    #

    account = forms.BooleanField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=ACCOUNT_CHOICES,
            attrs={
                'required': True,
            }
        ),
        required=False,
    )

    multilingual = forms.BooleanField(
        label='Ik ben',
        widget=forms.RadioSelect(
            choices=MULTILINGUAL_CHOICES,
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

    def clean(self):
        """
        Two tasks:

        Make sure the user has entered a name if creating an account.
        The field is not marked as required, as the requirement is conditional.

        Make sure the user has selected at least one of account/mailinglist
        """
        account = self.cleaned_data.get('account', False)
        name = self.cleaned_data.get('name', None)

        if account and not name:
            self.add_error('name', "Dit veld is verplicht")

        mailing_list = self.cleaned_data.get('mailing_list', False)

        if not account and not mailing_list:
            # It's an error on both, but we'll just add it to account as twice
            # is redundant
            self.add_error('account', "Kies a.u.b. om je in te schrijven voor "
                                      "de mailinglist en/of om een account aan "
                                      "te maken.")

        return self.cleaned_data

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

    def _html_output(self, normal_row, error_row, row_ender, help_text_html,
                     errors_on_separate_row):
        """This method overrides the default, but is mostly the same. It only
        filters out the 'account' and 'mailing_list' questions as we render
        those manually in the template."""

        # Errors that should be displayed above all fields.
        top_errors = self.non_field_errors().copy()
        output, hidden_fields = [], []

        for name, field in self.fields.items():

            # BEGIN ADDITION
            if name in ['account', 'mailing_list']:
                continue
            # END ADDITION

            html_class_attr = ''
            bf = self[name]
            bf_errors = self.error_class(bf.errors)
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {
                            'name':  name,
                            'error': str(e)
                        }
                         for e in bf_errors])
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % str(bf_errors))

                if bf.label:
                    label = conditional_escape(bf.label)
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % field.help_text
                else:
                    help_text = ''

                output.append(normal_row % {
                    'errors':          bf_errors,
                    'label':           label,
                    'field':           bf,
                    'help_text':       help_text,
                    'html_class_attr': html_class_attr,
                    'css_classes':     css_classes,
                    'field_name':      bf.html_name,
                })

        if top_errors:
            output.insert(0, error_row % top_errors)

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {
                        'errors':          '',
                        'label':           '',
                        'field':           '',
                        'help_text':       '',
                        'html_class_attr': html_class_attr,
                        'css_classes':     '',
                        'field_name':      '',
                    })
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))


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
