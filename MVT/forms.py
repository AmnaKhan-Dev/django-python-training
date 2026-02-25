from django import forms

class ContactForm(forms.Form):   # Normal Form
    name = forms.CharField(max_length=100)
    email = forms.EmailField()