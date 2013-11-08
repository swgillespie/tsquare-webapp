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
import os

dirname, filename = os.path.split(os.path.abspath(__file__))
GITHUB_BASE_AUTH_URL = 'https://github.com/login/oauth/authorize'
GITHUB_AUTH_EXCHANGE = 'https://github.com/login/oauth/access_token'
GOOGLE_BASE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_EXCHANGE_REDIRECT_URI = 'http://localhost:8000/google_login_exchange'
GOOGLE_OAUTH_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"

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
def profile(request):
	return render_to_response('profile.html')

@login_required
def resources(request):
	return render_to_response('resources.html')

@login_required
def gradebook(request):
	return render_to_response('gradebook.html')

@login_required
def github_login(request):
	f = open('github_config.txt','r')
	lines = f.readlines()
	f.close()
	params = {'client_id':lines[0].strip('\n')} # add client id here
	url = GITHUB_BASE_AUTH_URL+"?"+urllib.urlencode(params)
	return redirect(url)

@login_required
def github_login_exchange(request):
	f = open(dirname+'/github_config.txt','r')
	lines = f.readlines()
	f.close()
	params = {
		# add client id and secret here
		'client_id':lines[0].strip('\n'),
		'client_secret':lines[1].strip('\n'),
		'code':request.GET['code']
		}

	access_token = requests.post(GITHUB_AUTH_EXCHANGE,data=params)
	profile = UserProfile.objects.get(user_id=request.user.id)
	if len(profile.github_access_token) == 0:
		profile.github_access_token = access_token.text
		profile.save()
	return redirect('/external_services')

@login_required
def select_github_repos(request):
	profile = UserProfile.objects.get(user_id=request.user.id)
	if len(profile.github_access_token) == 0:
		return redirect('/external_services')
	return redirect('https://api.github.com/user/repos?'+profile.github_access_token)

# https://developers.google.com/accounts/docs/OAuth2Login
def google_login(request):
	f = open(dirname+'/google_config.txt','r')
	lines = f.readlines()
	f.close()
	params = {
		'client_id':lines[0].strip('\n'),
		'response_type':'code',
		'scope':'https://www.googleapis.com/auth/drive',
		'redirect_uri':GOOGLE_EXCHANGE_REDIRECT_URI
	}
	return redirect(GOOGLE_BASE_AUTH_URL+"?"+urllib.urlencode(params))

def google_login_exchange(request):
    code = request.GET['code']
    f = open(dirname+'/google_config.txt','r')
    lines = f.readlines()
    f.close()
    params = {
        'client_id':lines[0].strip('\n'),
        'client_secret':lines[1].strip('\n'),
        'code':code,
        'redirect_uri':GOOGLE_EXCHANGE_REDIRECT_URI,
        'grant_type':'authorization_code'
    }
    t = requests.post(GOOGLE_OAUTH_TOKEN_URL,data=params)
    profile = UserProfile.objects.get(user_id=request.user.id)
    if len(profile.gdrive_access_token) == 0:
		profile.gdrive_access_token = t['access_token']
		profile.save()
    return redirect('/external_services')

def gdrive_select(request):
    pass

@login_required
def external_services(request):
	return render(request,'external_services.html')

@login_required
def profile(request):
	return render(request,'profile.html')

@login_required
def list_assignments(request):
	tsapi = request.session['tsapi']
	sites = tsapi.get_sites()
	assignments = []
	for s in sites:
		assignments.append(tsapi.get_assignments(s))
	return HttpResponse(s)

@login_required
def course_info(request):
	return render_to_response('course_info.html')

@login_required
def announcements(request):
	return render_to_response('announcements.html')

@login_required
def wiki(request):
	return render_to_response('wiki.html')

@login_required
def help(request):
	return render_to_response('help.html')

@login_required
def assignment_detail(request):
	return render_to_response('assignment_detail.html')
