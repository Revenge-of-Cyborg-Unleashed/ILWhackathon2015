from django import forms

class SearchForm(forms.Form):
    destination = forms.CharField()
    departure = forms.CharField()
    outDate = forms.DateField(widget=forms.DateInput())
    inDate = forms.DateField(widget=forms.DateInput())
    emails = forms.EmailField()
    direct = forms.BooleanField()
