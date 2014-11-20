#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.core.exceptions import ValidationError
import models

class ServerForm(forms.ModelForm):
    class Meta:
        model = models.Server
        fields = ("servername",)


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('username', 'password')
        widgets = {'password': forms.PasswordInput()}
