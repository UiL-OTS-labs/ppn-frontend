from django import forms


class ChangeProfileForm(forms.Form):

    name = forms.Field()

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


class TimeSlotForm(forms.Form):

    datetime = forms.DateTimeField()

    max_places = forms.IntegerField()

    experiment = forms.Field(
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        super(TimeSlotForm, self).__init__(*args, **kwargs)

        self.fields['max_places'].widget.attrs.update(
            {
                'min': 1,
                'max': 10,
            }
        )
