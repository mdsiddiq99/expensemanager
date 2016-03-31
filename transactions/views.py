from django.shortcuts import render, render_to_response

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from users.models import UserProfile, UserAccounts
import json
from django.db.models import Q
from django.template import RequestContext
from transactions.models import Transaction, UserTransaction
# Create your views here.

userid = 2

@csrf_exempt
def make_transaction(request):
	resp = {}
	if request.method != 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Only POST allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')


	transaction_id = request.POST.get('transaction_id', '')
	amount = request.POST.get('amount', 0)
	account = request.POST.get('account', '')
	from_account = request.POST.get('from_account', '')
	to_account = request.POST.get('to_account', '')
	description = request.POST.get('description', '')
	date = request.POST.get('date', '')
	if not transaction_id:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'transaction id required'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	if not (account or from_account or to_account):
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'account required'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		transaction = Transaction.objects.get(id = transaction_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error %s' % e
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	if transaction.transaction_type =='income':
		if not to_account:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'account required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		try:
			ut = UserTransaction.objects.create(userprofile_id = userid, to_account_id = to_account, amount = amount, transaction_id = transaction_id, description = description)
			ua = UserAccounts.objects.get(id = to_account)
			ua.account_balance += long(amount)
			ua.save()

		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif transaction.transaction_type =='expense':
		if not from_account:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'account required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		try:
			ut = UserTransaction.objects.create(userprofile_id = userid, from_account_id = from_account, amount = amount, transaction_id = transaction_id, description = description)
			ua = UserAccounts.objects.get(id = from_account)
			ua.account_balance -= long(amount)
			ua.save()
		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif transaction.transaction_type =='transfer':
		if not to_account or not from_account:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'account required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		try:
			ut = UserTransaction.objects.create(userprofile_id = userid, to_account_id = to_account,from_account_id = from_account, amount = amount, transaction_id = transaction_id, description = description)
			ua = UserAccounts.objects.get(id = to_account)
			ua.account_balance += long(amount)
			ua.save()
			ua = UserAccounts.objects.get(id = from_account)
			ua.account_balance -= long(amount)
			ua.save()
		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif transaction.transaction_type =='balance reset':
		if not account:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'account required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		try:
			ut = UserTransaction.objects.create(userprofile_id = userid, account_id = account, amount = amount, transaction_id = transaction_id, description = description)
			ua = UserAccounts.objects.get(id = account)
			ua.account_balance = long(amount)
			ua.save()
		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	resp['status'] = 'success'
	resp['status_code'] = 200
	return HttpResponse(json.dumps(resp), content_type = 'application/json')

@csrf_exempt
def delete_transaction(request):
	resp = {}
	if request.method != 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Only POST allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	user_transaction_id = request.POST.get('user_transaction_id', '')


	if not user_transaction_id:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'transaction id required'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		user_transaction = UserTransaction.objects.select_related('transaction').get(id = user_transaction_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error %s' % e
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	old_amount = user_transaction.amount
	old_account = user_transaction.account
	old_from_account = user_transaction.from_account
	old_to_account = user_transaction.to_account
	old_description = user_transaction.description
	old_date = user_transaction.transaction_date

	if user_transaction.transaction.transaction_type =='income':
		try:
			ua = UserAccounts.objects.get(id = old_to_account)
			ua.account_balance -= long(old_amount)
			ua.save()

		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif user_transaction.transaction.transaction_type =='expense':
		try:
			ua = UserAccounts.objects.get(id = old_from_account)
			ua.account_balance += long(old_amount)
			ua.save()
		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif user_transaction.transaction.transaction_type =='transfer':
		try:
			ua = UserAccounts.objects.get(id = old_to_account)
			ua.account_balance -= long(old_amount)
			ua.save()
		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
	try:
		user_transaction.delete()
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error %s' % e
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	resp['status'] = 'success'
	resp['status_code'] = 200
	return HttpResponse(json.dumps(resp), content_type = 'application/json')

@csrf_exempt
def edit_transaction(request):
	resp = {}
	if request.method != 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Only POST allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')


	amount = request.POST.get('amount', 0)
	account = request.POST.get('account', '')
	from_account = request.POST.get('from_account', '')
	to_account = request.POST.get('to_account', '')
	description = request.POST.get('description', '')
	date = request.POST.get('date', '')
	user_transaction_id = request.POST.get('user_transaction_id', '')


	if not user_transaction_id:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'transaction id required'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	if not (account or from_account or to_account):
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'account required'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		user_transaction = UserTransaction.objects.select_related('transaction').get(id = user_transaction_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error %s' % e
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	old_amount = user_transaction.amount
	old_account = user_transaction.account
	old_from_account = user_transaction.from_account
	old_to_account = user_transaction.to_account
	old_description = user_transaction.description
	old_date = user_transaction.transaction_date

	if user_transaction.transaction.transaction_type =='income':
		if not to_account:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'account required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

		try:
			ua = UserAccounts.objects.get(id = old_to_account)
			ua.account_balance -= long(old_amount)
			ua.save()

			user_transaction.amount = amount
			user_transaction.to_account_id = to_account
			user_transaction.description = description

			ua = UserAccounts.objects.get(id = to_account)
			ua.account_balance += long(amount)
			ua.save()

		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif user_transaction.transaction.transaction_type =='expense':
		if not from_account:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'account required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		try:
			ua = UserAccounts.objects.get(id = old_from_account)
			ua.account_balance += long(old_amount)
			ua.save()

			user_transaction.amount = amount
			user_transaction.from_account_id = from_account
			user_transaction.description = description

			ua = UserAccounts.objects.get(id = from_account)
			ua.account_balance -= long(amount)
			ua.save()
		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif user_transaction.transaction.transaction_type =='transfer':
		if not to_account or not from_account:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'account required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		try:
			ua = UserAccounts.objects.get(id = old_to_account)
			ua.account_balance -= long(old_amount)
			ua.save()

			ua = UserAccounts.objects.get(id = old_from_account)
			ua.account_balance += long(old_amount)
			ua.save()

			user_transaction.amount = amount
			user_transaction.to_account_id = to_account
			user_transaction.from_account_id = from_account
			user_transaction.description = description

			ua = UserAccounts.objects.get(id = to_account)
			ua.account_balance += long(amount)
			ua.save()
			ua = UserAccounts.objects.get(id = from_account)
			ua.account_balance -= long(amount)
			ua.save()
		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif user_transaction.transaction.transaction_type =='balance reset':
		if not account:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'account required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		try:
			ua = UserAccounts.objects.get(id = account)
			ua.account_balance = long(amount)
			ua.save()
		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error %s' % e
			return HttpResponse(json.dumps(resp), content_type = 'application/json')

	resp['status'] = 'success'
	resp['status_code'] = 200
	return HttpResponse(json.dumps(resp), content_type = 'application/json')


def dashboard(request):
	resp = {}
	ts = Transaction.objects.all()
	uas = UserAccounts.objects.filter(userprofile_id = userid)
	uts = UserTransaction.objects.select_related('transaction').filter(Q(userprofile_id = userid, account__in = uas) | Q(userprofile_id = userid, to_account__in = uas) | Q(userprofile_id = userid, from_account__in = uas)).order_by('-created_on')
	transaction_types = []
	for t in ts:
		transaction_types.append({
				'id' : t.id,
				'type' : t.transaction_type
			})
	useraccounts = []
	for ua in uas:
		useraccounts.append({
				'id' : ua.id,
				'name' : ua.account_name,
				'balance' : ua.account_balance
			})
	usertransactions = []
	print len(uts)
	for ut in uts:
		if ut.transaction.transaction_type == 'income':
			usertransactions.append({
					'id' : ut.id,
					'transaction_id' : ut.transaction_id,
					'transaction_type' : ut.transaction.transaction_type,
					'to_account_id' : ut.to_account_id,
					'to_account_name' : ut.to_account.account_name,
					'amount' : ut.amount,
					'description' : ut.description,
					'date' :str(ut.transaction_date),
				})
		elif ut.transaction.transaction_type == 'expense':
			usertransactions.append({
					'id' : ut.id,
					'transaction_id' : ut.transaction_id,
					'transaction_type' : ut.transaction.transaction_type,
					'from_account_id' : ut.from_account_id,
					'from_account_name' : ut.from_account.account_name,
					'amount' : ut.amount,
					'description' : ut.description,
					'date' :str(ut.transaction_date),
				})
			
		elif ut.transaction.transaction_type == 'transfer':
			usertransactions.append({
					'id' : ut.id,
					'transaction_id' : ut.transaction_id,
					'transaction_type' : ut.transaction.transaction_type,
					'to_account_id' : ut.to_account_id,
					'to_account_name' : ut.to_account.account_name,
					'from_account_id' : ut.from_account_id,
					'from_account_name' : ut.from_account.account_name,
					'amount' : ut.amount,
					'description' : ut.description,
					'date' :str(ut.transaction_date),
				})
			
		elif ut.transaction.transaction_type == 'balance reset':
			usertransactions.append({
					'id' : ut.id,
					'transaction_id' : ut.transaction_id,
					'transaction_type' : ut.transaction.transaction_type,
					'account_id' : ut.account_id,
					'account_name' : ut.account.account_name,
					'amount' : ut.amount,
					'description' : ut.description,
					'date' :str(ut.transaction_date),
				})

	resp['status'] = 'success'
	resp['status_code'] = 200
	resp['accounts'] = useraccounts
	resp['transactions'] = usertransactions
	resp['transaction_types'] = transaction_types
	return render_to_response('dashboard.html', resp, context_instance=RequestContext(request))

