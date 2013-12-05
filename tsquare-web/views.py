# Create your views here.

from django.shortcuts import render,render_to_response,redirect
from tsquare.core import TSquareAPI, TSquareAuthException
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from models import *
import urllib
import requests
import os

dirname, filename = os.path.split(os.path.abspath(__file__))
GITHUB_BASE_AUTH_URL = 'https://github.com/login/oauth/authorize'
GITHUB_AUTH_EXCHANGE = 'https://github.com/login/oauth/access_token'
GOOGLE_BASE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_EXCHANGE_REDIRECT_URI = 'http://tsquare-webapp-temp.herokuapp.com/google_login_exchange'
GOOGLE_OAUTH_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"

def tlogin(request):
    """
    Logs into a user's T-square account by authenticating their credentials using T-square API
    """
    if(request.method == 'POST'):
            username = request.POST['username']
            password = request.POST['password']
            try:
                tsapi = TSquareAPI(username, password)
                request.session['tsapi'] = tsapi
                request.session['courses'] = tsapi.get_sites()
            except TSquareAuthException:
                return render(request,'login.html',{'login_failed':'Invalid username or password.'})
            try:
                user = User.objects.get(username=username)
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/home/')
                else:
                    user = User.objects.get(username=username)
                    user.password = password
                    user.save()
		    user = authenticate(username=username, password=password)
		    login(request,user)
                    return redirect('/home/')
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
     """
     Logs out of a user's T-square account
     """
	logout(request)
	return redirect('/')

@login_required
def home(request):
        '''
        A home screen view that displays current semester's courses in the 
        navbar and sets user's current course to the first available course.
        '''
        tsapi = request.session['tsapi']
        user = tsapi.get_user_info()
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
        # set current course to first by default
        profile = UserProfile.objects.get(user_id=request.user.id)
        profile.current_course = curr_sites[0]
        profile.save()
        return render_to_response('home.html',{'userinfo'  :user,
                                               'curr_sites':curr_sites})

@login_required
def profile(request):
        tsapi = request.session['tsapi']
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
    	return render(request,'profile.html',{'curr_sites':curr_sites})

@login_required
def resources(request):
        tsapi = request.session['tsapi']
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
    	return render(request,'resources.html',{'curr_sites':curr_sites})

@login_required
def gradebook(request):
        tsapi = request.session['tsapi']
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
        # arbitrarily gets grades from first current sites for 
        site = curr_sites[0]
        grades = tsapi.get_grades(site)
    	return render(request,'gradebook.html',{'grades'    :grades,
                                                'curr_sites':curr_sites})

@login_required
def github_login(request):
    """
    Allows the user to authenticate T-square to use his or her Github account
    """
        profile = UserProfile.objects.get(user_id=request.user.id)
        if len(profile.github_access_token) != 0:
            return redirect('/services?done=already&service=GitHub')
        f = open(dirname+'/github_config.txt','r')
        lines = f.readlines()
        f.close()
        params = {'client_id':lines[0].strip('\n')} # add client id here
        url = GITHUB_BASE_AUTH_URL+"?"+urllib.urlencode(params)
        return redirect(url)

@login_required
def github_login_exchange(request):
    """
    Obtains an access token for a user's Github account in order to make requests on his or her behalf
    """
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
        profile.github_access_token = access_token.text
        profile.save()
        return redirect('/services?done=new&service=GitHub')

@login_required
def select_github_repos(request):
	profile = UserProfile.objects.get(user_id=request.user.id)
	if len(profile.github_access_token) == 0:
		return redirect('/services')
	return redirect('https://api.github.com/user/repos?'+profile.github_access_token)

# https://developers.google.com/accounts/docs/OAuth2Login
@login_required
def google_login(request):
    """
    Allows the user to authenticate T-square to use his or her Google Drive account
    """
        profile = UserProfile.objects.get(user_id=request.user.id)
        if len(profile.gdrive_access_token) != 0:
            return redirect('/services?done=already&service=Google Drive')
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

@login_required
def google_login_exchange(request):
    """
    Obtains an access token for a user's Google Drive account in order to make requests on his or her behalf
    """
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
        profile.gdrive_access_token = t.json()['access_token']
        profile.save()
        return redirect('/services?done=new&service=Google Drive')

@login_required
def gdrive_select(request):
    pass

@login_required
def external_services(request):
    """
    Shows all the external services a user can integrate his or her account with
    """
    params = {}
    if 'done' in request.GET:
        if request.GET['done'] == 'already':
            params['notice_already'] = 'You have already integrated your account with '+request.GET['service']
        else:
            params['notice_new'] = 'You have successfully integrated your account with '+request.GET['service']+'!'
    return render(request,'external_services.html',params) # how to pass in site list here?

@login_required
def sites(request):
        tsapi = request.session['tsapi']
        sites = tsapi.get_sites()
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
        return render(request,'sites.html',{'curr_sites':curr_sites,
                                            'sites'     :sites})

@login_required
def assignments(request):
        '''
        An example assignments view that gets assignments from the first current semester.
        '''
        tsapi = request.session['tsapi']
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
        site = curr_sites[0]
        assignments = tsapi.get_assignments(site)
        return render(request,'assignments.html',{'assignments':assignments,
                                                  'curr_sites' :curr_sites})

@login_required
def course_info(request):
        '''
        A view for the course info page with a proof of concept for switching 
        the current course by clicking on the navbar course links. Note: this 
        feature only works on the course info page at the moment.
        '''
        tsapi = request.session['tsapi']
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
        # save current course on click
        profile = UserProfile.objects.get(user_id=request.user.id)
        for site in curr_sites:
            if (request.GET.get(site.id)):
                profile.current_course = site.title
                profile.save()
        curr = profile.current_course
        return render_to_response('course_info.html',{'curr_sites':curr_sites,'curr':curr})

@login_required
def announcements(request):
        tsapi = request.session['tsapi']
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
        return render(request,'announcements.html',{'curr_sites':curr_sites})

@login_required
def wiki(request):
        tsapi = request.session['tsapi']
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
        return render(request,'wiki.html',{'curr_sites':curr_sites})

@login_required
def help(request):
        tsapi = request.session['tsapi']
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
        return render(request,'help.html',{'curr_sites':curr_sites})

@login_required
def assignment_detail(request):
        tsapi = request.session['tsapi']
        curr_sites = tsapi.get_sites(filter_func=get_curr_sites)
        return render(request,'assignment_detail.html',{'curr_sites':curr_sites})

def get_curr_sites(site):
        '''
        A filter function that returns true if the parameter site is from the  current semester
        '''
        time = timezone.now()
        if time.month < 6:
            curr_term = 'SPRING ' + str(time.year)
        else:
            curr_term = 'FALL ' + str(time.year)
        if site.props['term'] == curr_term:
            return True
        else:
            return False

def help(request):
    """
    Shows a documentation for T-square to the user
    """
    return render(request,'help.html')