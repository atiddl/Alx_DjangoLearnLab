from django import forms

class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)

class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message")
