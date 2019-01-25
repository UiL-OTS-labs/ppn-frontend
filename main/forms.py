from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _

from api.resources.account_resources import ChangePassword


class ChangePasswordForm(forms.Form):

    error_messages = {
        'password_mismatch': _("forms:change_password:password_mismatch"),
        'password_incorrect': _("forms:change_password:password_incorrect"),
    }

    new_password1 = forms.CharField(
        label=_('forms:change_password:new1'),
        strip=False,
        widget=forms.PasswordInput
    )

    new_password2 = forms.CharField(
        label=_('forms:change_password:new2'),
        strip=False,
        widget=forms.PasswordInput
    )

    old_password = forms.CharField(
        label=_('forms:change_password:old'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autofocus': True
        }),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch'
                )

        password_validation.validate_password(password2)

        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password1')

        # If we already have errors on record from the new password fields,
        # we shouldn't do the request.
        if self.errors:
            return old_password

        req = ChangePassword()
        req.current_password = old_password
        req.new_password = new_password

        response = req.put()

        if not response.success:
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )

        return old_password