from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import mail
import uuid
from django.db import models
from django.contrib.auth.models import User
from .models import Member, ActivationData
from gamecenter.models import Game
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
import logging
logger = logging.getLogger(__name__)
class GameAddForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['game_name','price','game_description','developer']

class GameUpdateForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['game_name','price','game_description']

class GameDeleteForm(forms.ModelForm):

    actions = (
        ('delete', 'delete'), #how about adding modify action or new actions
    )
    choice = forms.MultipleChoiceField(required=False,
                                       widget=forms.CheckboxSelectMultiple,
                                       choices=actions,
                                       )
    class Meta:
        model = Game
        fields = ['game_name','price','game_description']

class member_register(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    user_type = (
        ('players', 'player'),
        ('developers', 'developer'),
        ('', 'None'),
    )
    group =  forms.ChoiceField(label='Account type',choices=user_type, required=True,)
    class Meta:
        model = Member
        fields = ('email', 'username','first_name','last_name',) #what else ? Street address.....
    #requires validation
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        #check if user exists. 
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(member_register, self).save(commit=False)
        user.email  = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            chosen = self.cleaned_data.get("group")
            #group = Group.objects.get_or_create(name=chosen)
            group = Group.objects.get(name=chosen)
            user.groups.add(group)

            eemail  = self.cleaned_data.get("email")
            code =str(uuid.uuid4())[0:24]
            mailer(self,code,eemail)
            #activation code is saved for future reference
            active = ActivationData.objects.filter(email=eemail)
            if not active:
                ActivationData.objects.create(member=user,email=eemail, activation_code=code).save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Member
        fields = ('email', 'password','first_name','last_name', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class loginForm(forms.Form):
    email       = forms.CharField(label='email')
    password    = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        #get values from the form
        username        = self.cleaned_data.get("email") #username is an email
        password        = self.cleaned_data.get("password")
        #retrieve user from db.
        user = Member.objects.filter(email=username)
        if not user:
            raise forms.ValidationError("In valid username or password") #do not get specific
        else:
            user = Member.objects.filter(email=username).first()#get it out
            if user.check_password(password):
                #match found
                #check if account is activated.
                if not user.is_active:
                    pass
                    #do we let him login  ?NO, but allow him to get a new activation key
                    raise forms.ValidationError("In active account, please check your email for the activation code")
                #an active account
                return super(loginForm, self).clean(*args, **kwargs)
            else:
                raise forms.ValidationError("In valid username or password") #do not get specific

class ActivationForm(forms.Form):
    email   = forms.CharField(label='email')
    code    = forms.CharField(label='Activation code') #code

    def clean(self,*args,**kwargs):
        #get values from the form
        email        = self.cleaned_data.get("email") #username is an email
        code         = self.cleaned_data.get("code")
        #retrieve user from db.
        user = ActivationData.objects.filter(email__iexact=email)
        if not user:
            raise forms.ValidationError("unknown email, please make a registration.") #do not get specific
        else:
            user = ActivationData.objects.filter(email=email).first()#get it out
            logger.debug(user.activation_code)
            logger.debug(code)
            if not user.activation_code == code:
                raise forms.ValidationError("Incorrect activation key.")

            else: #activate the account
                    #no need to check again, if active, would not hurt to activate it again.
                    logger.debug("We are activating your account. ....")
                    account = Member.objects.filter(email=email).first()#get it out
                    account.is_active = True
                    account.save()
                    #an active account
        return super(ActivationForm, self).clean(*args, **kwargs)

def mailer(self,code,email):
    connection = mail.get_connection()
    # Manually open the connection
    connection.open()
    # Construct an email message that uses the connection
    email1 = mail.EmailMessage(
        'Activation code for '+email,
        'Please use this code to activate your account: ' + code,
        'admin@gamestore.com',
        [email],
        connection=connection,
        )
    email1.send()  # Send the email
