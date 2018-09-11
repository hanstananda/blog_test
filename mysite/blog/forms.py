from django import forms


class NameForm(forms.Form):
    email = forms.CharField(label='E-mail address', max_length=25)
    password = forms.CharField(label='Password', max_length=25)
