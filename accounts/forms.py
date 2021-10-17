
from django import forms
from .models import *


class EditUserProfileForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last name'})) 
	phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
	short_description = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Description'}))
	profile_picture = forms.ImageField(label='Image Profile',widget=forms.FileInput)

	class Meta:
		model = Profile
		fields = (
			'first_name',
			'last_name',
			'phone',
			'short_description',
			'profile_picture'
			)