# Create your views here.

from django.shortcuts import render,render_to_response,redirect
from tsquare_api import TSquareAPI, TSquareAuthException
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def tlogin(request):
	if(request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		try:
		    tsapi = TSquareAPI(username, password)
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
		    return redirect('/home/')
    	return render(request,'login.html')

def tlogout(request):
	logout(request)
	return redirect('/')

def index(request):
	return render_to_response('index.html')

@login_required	
def home(request):
	return render_to_response('home.html')
