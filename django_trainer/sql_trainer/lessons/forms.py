from django import forms
from .models import Exercise

class QueryForm(forms.Form):
    """Form for executing SQL queries"""
    query = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'sql-editor',
            'rows': 10,
            'style': 'font-family: monospace; width: 100%;',
            'placeholder': 'Enter your SQL query here...',
        }),
        required=True
    )
    
    def __init__(self, *args, initial_query=None, **kwargs):
        super().__init__(*args, **kwargs)
        if initial_query:
            self.fields['query'].initial = initial_query