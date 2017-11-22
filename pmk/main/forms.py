# coding: utf-8

import datetime

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
	
	class Meta:
		model = Order
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': u'Стив Джобс*', 'required': True}),
			'tel': forms.TextInput(attrs={'placeholder': u'(___) ___-____*', 'type': 'tel', 'required': True}),
			'email': forms.TextInput(attrs={'placeholder': u'steve@apple.com*', 'required': True}),
			'comment': forms.Textarea(attrs={'placeholder': u'Не звоните с 14:00 до 15:00, пожалуйста'}),
			'delivery_date': forms.TextInput(attrs={'required':True}),
			'order': forms.TextInput(attrs={'type':'hidden', 'required':True}),
		}
		labels = {
            'tel':u'Телефон без +7',
        }
		exclude = ('total',)

	def clean_delivery_date(self):
		date = self.cleaned_data['delivery_date']
		#delivery_date = datetime.datetime.strptime(data, '%Y-%m-%d') 
		if (date.weekday() not in (2,4)) or date == datetime.datetime.now():
			raise forms.ValidationError(u'Заказ возможен только на среду и пятницу, но не день в день')

		return date