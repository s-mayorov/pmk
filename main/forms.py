# coding: utf-8

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
	
	class Meta:
		model = Order
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': u'Стив Джобс*', 'required': True}),
			'tel': forms.TextInput(attrs={'placeholder': u'(___) ___-____*', 'required': True}),
			'email': forms.TextInput(attrs={'placeholder': u'steve@apple.com*', 'required': True}),
			'comment': forms.Textarea(attrs={'placeholder': u'Не звоните с 14:00 до 15:00, пожалуйста'}),
			'delivery_date': forms.TextInput(attrs={'required':True}),
			'order': forms.TextInput(attrs={'type':'hidden', 'required':True}),
		}
		labels = {
            'tel':u'Телефон без +7',
        }
		exclude = ()
