# Create your views here.

from django.shortcuts import render,render_to_response,redirect
from tsquare.core import TSquareAPI, TSquareAuthException
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import *
import urllib
import requests

def tlogin(request):
	if(request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		try:
		    tsapi = TSquareAPI(username, password)
		    request.session['tsapi'] = tsapi
		except TSquareAuthException:
		    return render(request,'login.html')
		try:
		    user = User.objects.get(username=username)
		    user = authenticate(username=username, password=password)
		    if user is not None:
			login(request, user)
			print "returning redirect home after auth..."
			return redirect('/home/')
		    else:
			return render(request,'login.html')
		except User.DoesNotExist:
		    # get username and email from tsapi. leave password blank
		    user = User.objects.create_user(username, tsapi.get_user_info().email, password) 
		    profile = UserProfile(user=user)
		    profile.save()
		    user = User.objects.get(username=username)
		    ua = authenticate(username=username,password=password)
		    if ua is not None:
			login(request,ua)
		    	return redirect('/home/')
		    else:
			print 'new user created auth failed...'
	return render(request,'login.html')

def tlogout(request):
	logout(request)
	return redirect('/')

def index(request):
	return render_to_response('index.html')

@login_required	
def home(request):
	return render_to_response('home.html')

@login_required
def github_login(request):
	u = 'https://github.com/login/oauth/authorize'
	params = {'client_id' : '9a5505bd7e9f1db972e5'}
	url = u+"?"+urllib.urlencode(params)
	return redirect(url)

@login_required
def github_login_exchange(request):
	u = 'https://github.com/login/oauth/access_token'
	params = {
		# add client id and secret here
		'code':request.GET['code'],
        'client_id' : '9a5505bd7e9f1db972e5',
        'client_secret' : '04f73195dd350a52f509874262b0163aa375381e'
		}
	
	access_token = requests.post(u,data=params)
	profile = UserProfile.objects.get(user_id=request.user.id)
	if len(profile.github_access_token) == 0:
		profile.github_access_token = access_token.text
		profile.save()
	return redirect('/setup_profile')

@login_required
def select_github_repos(request):
	profile = UserProfile.objects.get(user_id=request.user.id)
	if len(profile.github_access_token) == 0:
		return redirect('/setup_profile')
	return redirect('https://api.github.com/user/repos?'+profile.github_access_token)

@login_required
def setup_profile(request):
	return render(request,'setup_profile.html')

@login_required
def list_assignments(request):
	tsapi = request.session['tsapi']
	sites = tsapi.get_sites()
	assignments = []
	for s in sites:
		assignments.append(tsapi.get_assignments(s))
	return HttpResponse(s)
