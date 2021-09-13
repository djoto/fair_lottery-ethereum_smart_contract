from django import forms
from decimal import Decimal

class FormCreate(forms.Form):
    account_address = forms.CharField(label='Your account address:', max_length=100)
    num_of_participants = forms.IntegerField(label='Number of possible participants:', min_value=2, max_value=1000)
    amount_to_invest = forms.DecimalField(label='Amount to invest (ether cryptocurrency):', widget=forms.NumberInput(attrs={'step': 0.0000001}), min_value=Decimal(0.0000001))
    private_key = forms.CharField(label='Your private key:', widget=forms.PasswordInput, max_length=100)
    

class FormJoin(forms.Form):
    account_address = forms.CharField(label='Your account address:', max_length=100)
    lottery_id = forms.CharField(label='Lottery ID:', max_length=100)
    amount_to_invest = forms.DecimalField(label='Amount to invest (ether cryptocurrency):', widget=forms.NumberInput(attrs={'step': 0.0000001}), min_value=Decimal(0.0000001))
    private_key = forms.CharField(label='Your private key:', widget=forms.PasswordInput, max_length=100)
