from django import forms

class SearchForm(forms.Form):
    departure = forms.CharField(label='Departure')
    destination = forms.CharField(label='Destination')
    trips_date = forms.DateField(label='Date')
