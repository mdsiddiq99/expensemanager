# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20160331_0206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_type', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('transaction_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=100, null=True, blank=True)),
                ('account', models.ForeignKey(related_name='account', to='users.UserAccounts', null=True)),
                ('from_account', models.ForeignKey(related_name='from_account', to='users.UserAccounts', null=True)),
                ('to_account', models.ForeignKey(related_name='to_account', to='users.UserAccounts', null=True)),
                ('transaction', models.ForeignKey(to='transactions.Transaction')),
                ('userprofile', models.ForeignKey(to='users.UserProfile')),
            ],
        ),
    ]
