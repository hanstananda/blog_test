from django import forms


class NameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=25)
    password = forms.CharField(label='Password', max_length=25)


class EditCategoryForm(forms.Form):
    category_name = forms.CharField(label='category', max_length=100)
    category_id = forms.HiddenInput()

