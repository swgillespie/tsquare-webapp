'''
Created on Aug 28, 2013

@author: Nirav
'''

from django.contrib.auth.models import User
from tsquare_api import TSquareAPI, TSquareAuthException

class TSquareAuthBackend(object):
    '''
    classdocs
    '''
    
    def authenticate(self, username=None, password=None):
        
        try:
            tsapi = TSquareAPI(username, password)
        except TSquareAuthException:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # get username and email from tsapi. leave password blank
            user = User.objects.create_user(username, email, password) 
        return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
