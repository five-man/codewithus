from socket import fromshare
from django import forms
from .models import Algorithm

class AlgoForm(forms.ModelForm):
    class Meta:
        model = Algorithm
        fields = ['algo_title', 'algo_detail', 'tag_id']
        labels = {
            
        }