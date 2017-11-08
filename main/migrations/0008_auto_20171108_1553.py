# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20171108_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='Электронная почта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=True, verbose_name='В наличии'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу'),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order',
            field=models.TextField(blank=True, verbose_name='Содержимое заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='tel',
            field=models.CharField(blank=True, max_length=50, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('1', 'Молоко'), ('2', 'Сыр'), ('3', 'Йогурт'), ('4', 'Кефир'), ('5', 'Творог')], max_length=1, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='expiration',
            field=models.PositiveIntegerField(verbose_name='Срок годности (сут.)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pack',
            field=models.CharField(choices=[('1', 'ПЭТ'), ('2', 'пластиковый конт.'), ('3', 'пластиковый стакан запайка / крышка'), ('4', 'Кусок, вакуум')], max_length=1, verbose_name='Тип упаковки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='volume',
            field=models.PositiveIntegerField(verbose_name='Объём/Вес ед. упаковки, мл/гр'),
        ),
    ]
