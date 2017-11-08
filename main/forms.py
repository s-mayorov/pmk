# coding: utf-8

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
	
	class Meta:
		model = Order
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': u'Имя*', 'required': True}),
			'tel': forms.TextInput(attrs={'placeholder': u'Телефон*', 'required': True}),
			'delivery_date': forms.TextInput(attrs={'required':True}),
			'order': forms.TextInput(attrs={'type':'hidden', 'required':True}),
		}
		exclude = ()
