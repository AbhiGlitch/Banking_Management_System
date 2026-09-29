from django import forms
from django.contrib.auth.models import User
from .models import BankAccount


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = [
            'account_type',
            'phone',
            'address'
        ]
class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12,decimal_places=2,min_value=0.01,label="Deposit Amount")        
class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12,decimal_places=2,min_value=0.01,label="Withdraw Amount")
class TransferForm(forms.Form):
    receiver_account_number = forms.CharField(max_length=12,label="Receiver Account Number")
    amount = forms.DecimalField(max_digits=12, decimal_places=2,min_value=0.01,label="Transfer Amount")