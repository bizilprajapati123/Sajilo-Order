from django import forms
from .models import MyUser, ReportUser

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(min_length=3, max_length=70)
    username = forms.CharField(min_length=5, max_length=70)
    date_of_birth = forms.DateField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone_number = forms.IntegerField(max_value=9999999999, min_value=9800000000)
    password = forms.CharField(min_length=7, max_length=70, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=7, max_length=70, widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = [
            "email",
            "username",
            "date_of_birth",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "VatPan_number",
            "OwnerProof",
            "shop_name",
            "password",
            "password2",
        ]

    # password validation
    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("passwords fields did not match")


class VendorUserUpdateform(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ["shop_name", "first_name", "last_name", "phone_number"]


class UserUpdateform(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ["first_name", "last_name", "phone_number"]


class ReportUserForm(forms.ModelForm):
    class Meta:
        model = ReportUser
        fields = ["proof", "reason", "usernames"]
