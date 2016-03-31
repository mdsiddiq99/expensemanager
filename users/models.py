from django.db import models

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField('auth.User', null = True)
	name = models.CharField(max_length = 100, null = True, blank = True)


class UserAccounts(models.Model):
	userprofile = models.ForeignKey(UserProfile, null = False)
	account_name = models.CharField(max_length = 100, null = True, blank = True)
	account_balance = models.IntegerField(default = 0)
	created_on = models.DateTimeField(auto_now_add = True, null = True)

	class Meta:
		unique_together = ('userprofile', 'account_name')
