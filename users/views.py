from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from users.models import UserProfile, UserAccounts
import json
from transactions.models import Transaction, UserTransaction
# Create your views here.r

userid = 2

@csrf_exempt
def create_account(request):
	resp = {}
	if request.method != 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Only POST allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')


	name = request.POST.get('name', '')
	balance = request.POST.get('balance', 0)
	print request.POST
	if not name:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'name required'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		ua = UserAccounts.objects.update_or_create(userprofile_id = userid, account_name = name, defaults = {'account_balance':balance})
		print ua
		# ua.account_balance = balance
		# ua.save()
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error %s' % e
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	resp['status'] = 'success'
	resp['status_code'] = 200
	# resp['account_id'] = ua.id
	# resp['account_name'] = ua.account_name
	# resp['account_balance'] = ua.account_balance

	return HttpResponse(json.dumps(resp), content_type = 'application/json')

@csrf_exempt
def delete_account(request):
	resp = {}
	if request.method != 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Only POST allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	return

@csrf_exempt
def edit_account(request):
	resp = {}
	if request.method != 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Only POST allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	return
