from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm)
from django.contrib.auth.models import User

from polls.models import Option, Polls


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        emailed = User.objects.filter(email=email).exists()
        if emailed is True:
            raise forms.ValidationError('Please use another email')
        return email
    
    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This Username Already Exists Use another email')
        return username

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Username','id':'loginpwd'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
    'placeholder':'Password','id':'login-pwd'}
    ))


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email',max_length=200,widget= forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'email','id':'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError("Unfortunately we can't find your email address")
        return email

class PwdResetConfirm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password','id':'form-new-pass1'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class CreatePollForm(forms.ModelForm):
    choice_text1 = forms.CharField(label='Choice 1',max_length=250, required=True)
    choice_text2 = forms.CharField(label='Choice 2',max_length=250, required=True)
    class Meta:
        model = Polls
        fields = ['title','description','choice_text1','choice_text2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Title'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Option 1'})
        self.fields['choice_text1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Option 2'})
        self.fields['choice_text2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Description of the poll'})


class OptionPollForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['option'].widget.attrs.update(
            {'class':'form-control mb-3','placeholder':'Choices'}
        )

class EditPollForm(forms.ModelForm):
    class Meta:
        model = Polls
        fields= ['title']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }

class OptionEditForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option',]
        widget={
            'option':forms.TextInput(attrs={'class':'form-control'})
        }