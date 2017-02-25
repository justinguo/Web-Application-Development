import sys
from django import forms

from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from django.forms import ModelForm
from socialnetwork.models import *

class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label = 'Email',
                                widget = forms.EmailInput(
                                    attrs = {'class' : 'form-control'}))

class NewSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label = "New password",
                                        widget = forms.PasswordInput(
                                            attrs = {'class' : 'form-control'}))
    new_password2 = forms.CharField(label = "New password confirmation",
                                        widget = forms.PasswordInput(
                                            attrs = {'class' : 'form-control'}))

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20,
    			                 widget = forms.TextInput(
    							 attrs={'class' : 'form-control',
    									'placeholder' : 'New Username'}))
    password1 = forms.CharField(max_length = 200, 
    							label = 'Password',
                                widget = forms.PasswordInput(
                                attrs={'class' : 'form-control',
                                		   'placeholder' : 'New Password'}))
    password2 = forms.CharField(max_length = 200,
    							label = 'Confirm Password',
                                widget = forms.PasswordInput(
                                	attrs={'class' : 'form-control',
                                		   'placeholder' : 'Retype Password'}))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if (password1 and password2 and password1 != password2):
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already exist.")

        return username

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder' : 'Username',
        }))
    password = forms.CharField(widget = forms.PasswordInput(
        attrs={'class' : 'form-control',
               'placeholder' : 'Password',
        }))

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['profile', 'dislikes', 'posted_at']
        labels = {
            'title' : 'Post Title',
            'textpost' : 'Description',
            'image' : 'Attach Image'
        }
        widgets = {
            'image' : forms.FileInput(),
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'id' : 'title',
                'placeholder' : 'Max 100 character limit'}),
            'textpost' : forms.Textarea(attrs={'class' : 'form-control',
                'id' : 'description', 'placeholder' : 'Max 400 character limit', 
                'maxlength' : 400, 'rows' : 4})
        }

class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length = 20,
                                 label='First Name',
                                 help_text='20 characters max.')
    last_name = forms.CharField(max_length = 20,
                                label='Last Name',
                                help_text='20 characters max.')
    password = forms.CharField(label='Current Password',
                                required=False,
                                widget=forms.PasswordInput(
                                    attrs={'class' : 'form-control',
                                            'id' : 'inputPassword1',
                                            'placeholder' : 'Type Your Current Password...'}))
    password1 = forms.CharField(label='New Password',
                                required=False,
                                widget=forms.PasswordInput(
                                    attrs={'class' : 'form-control',
                                            'id' : 'inputPassword2',
                                            'placeholder' : 'Type New Password...'}))
    password2 = forms.CharField(label='Confirm Password',
                                required=False,
                                widget=forms.PasswordInput(
                                    attrs={'class' : 'form-control',
                                            'id' : 'inputPassword3',
                                            'placeholder' : 'Retype New Password...'}))

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'followers']
        labels = {
            'img' : 'Upload Profile Picture',
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'age' : 'Age',
            'birthday' : 'Birthday',
            'self_description' : 'Bios',
        }
        widgets = { 
            'img' : forms.FileInput(),
            'age' : forms.NumberInput(attrs={'class' : 'form-control', 'id' : 'age'}),
            'birthday' : forms.DateInput(attrs={'class' : 'form-control', 'id' : 'birthday', 'type' : 'date'}),
            'self_description' : forms.Textarea(attrs={'class' : 'form-control', 'maxlength' : 400, 'id' : 'description', 'placeholder' : '400 max character limit'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        if ('upload-pw' in self.data):
            password = cleaned_data['password']            
            password1 = cleaned_data['password1']
            password2 = cleaned_data['password2']

            if (not password or not password1 or not password2):
                raise forms.ValidationError("Password fields are empty!")

            if (password and not check_password(password, self.user.password)):
                raise forms.ValidationError("Password is not correct!")
        
            if (password1 and password2 and password1 != password2):
                raise forms.ValidationError("Passwords are not match!")

        if ('upload-info' in self.data):
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            age = cleaned_data.get('age')
            birthday = cleaned_data.get('birthday')
            self_description = cleaned_data.get('self_description')

            if (not first_name or not last_name or not age or not birthday or not self_description):
                raise forms.ValidationError("Personal information fields should be complete!")

        return cleaned_data
