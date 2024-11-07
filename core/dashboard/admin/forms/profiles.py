from django import forms
from profiles_app.models import AdminProfile
from django.contrib.auth.forms import PasswordChangeForm

class AdminChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Invalid old password.')
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('New passwords do not match.')

        return new_password2

class AdminProfileForm(forms.ModelForm):

    class Meta:
        model = AdminProfile
        fields = [
            "first_name",
            "last_name",
        ]



class AdminProfileImageForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = [
            "image",
        ]


