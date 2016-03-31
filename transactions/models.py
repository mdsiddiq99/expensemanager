from django.db import models

from users.models import UserProfile, UserAccounts
# Create your models here.
class Transaction(models.Model):
	transaction_type = models.CharField(max_length = 100, null = True, blank = True)


class UserTransaction(models.Model):
	userprofile = models.ForeignKey(UserProfile, null = False)
	account = models.ForeignKey(UserAccounts, null = True, related_name = 'account')
	from_account = models.ForeignKey(UserAccounts, null = True, related_name = 'from_account')
	to_account = models.ForeignKey(UserAccounts, null = True, related_name = 'to_account')
	created_on = models.DateTimeField(auto_now_add = True, null = True)
	transaction_date = models.DateTimeField(auto_now_add = True, null = True)
	transaction = models.ForeignKey(Transaction, null = False)
	amount = models.IntegerField(default = 0)
	description = models.CharField(max_length = 100, null = True, blank = True)
