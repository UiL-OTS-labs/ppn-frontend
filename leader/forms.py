from django import forms


class ChangeProfileForm(forms.Form):

    name = forms.Field()

    # TODO: decide if to remove this
    email = forms.EmailField(required=False)

    phone = forms.Field()

    photo = forms.ImageField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'disabled': 'disabled'
        })