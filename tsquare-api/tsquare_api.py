import requests

BASE_URL_GATECH = 'https://login.gatech.edu/cas/'
SERVICE = 'https://t-square.gatech.edu/sakai-login-tool/container'
BASE_URL_TSQUARE = 'https://t-square.gatech.edu/direct/'

class TSquareException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
        
class TSquareAuthException(TSquareException):
    pass

class NotAuthenticatedException(TSquareException):
    pass
    
class TSquareAPI(object):
    def requires_authentication(func):
        '''
        Function decorator that throws an exception if the user
        is not authenticated, and executes the function normally
        if the user is authenticated.
        '''
        def _auth(self, *args, **kwargs):
            if not self._authenticated:
                raise NotAuthenticatedException('Function {} requires' +
                                                'authentication'
                                                .format(func.__name_))
            else:
                return func(self, *args, **kwargs)
        return _auth

    def attributes(**kwargs):
        '''
        Function decorator that adds some metadata to functions.
        '''
        def _decorate(func):
            for key in kwargs:
                setattr(func, key, kwargs[key])
            return func
        return _decorate


    def __init__(self, username, password):
        '''
        Initialize a TSquareAPI object. Attempts to log in with the given
        username and password.
        @param username - The username to log in with
        @param password - The password to log in with. Not stored.

        @throws TSquareAuthException - If something goes wrong during the
        authentication process.
        '''
        self.username = username
        self._tg_ticket, self._service_ticket = _get_ticket(username, password)
        self._session = _tsquare_login(self._service_ticket)
        self._authenticated = True

    @attributes(version_added='0.1',
                author='Sean Gillespie')
    @requires_authentication
    def get_user_info(self):
        '''
        Returns a TSquareUser object representing the currently logged in user.
        Throws a NotAuthenticatedException if the user is not authenticated.
        '''
        response = self._session.get(BASE_URL_TSQUARE + '/user/current.json')
        response.raise_for_status() # raises an exception if not 200: OK
        user_data = response.json()
        del user_data['password'] # tsquare doesn't store passwords
        return TSquareUser(**user_data)

    @attributes(version_added='0.1',
                author='Sean Gillespie')
    @requires_authentication
    def get_sites(self, filter_func=None):
        '''
        Returns a list of TSquareSite objects that represent the sites available
        to a user.
        @param filter_func - A function taking in a Site object as a parameter
                             that returns a True or False, depending on whether
                             or not that site should be returned by this
                             function. Filter_func should be used to create
                             filters on the list of sites (i.e. user's
                             preferences on what sites to display by default).
                             If not specified, no filter is applied.
        @returns - A list of TSquareSite objects encapsulating t-square's JSON
                   response.
        '''
        response = self._session.get(BASE_URL_TSQUARE + '/direct/site.json')
        response.raise_for_status() # raise an exception if not 200: OK
        site_list = response.json()['site_collection']
        if site_list == []:
            # this is an indication that the user is either not logged in or
            # the session expired. Either way, it's bad news. Probably
            # throw an exception here or something. -Sean
            pass
        if filter_func:
            return filter(filter_func,
                          map(lambda x: TSquareSite(**x), site_list))
        else:
            return map(lambda x: TSquareSite(**x), site_list)

class TSquareUser:
    def __init__(self, **kwargs):
        '''
        Encapsulates the raw JSON dictionary that represents a user in TSquare.
        Converts a dictionary to attributes of an object for ease of use.
        This constructor should never be called directly; instead, it is
        called by get_user_info.
        '''
        for key in kwargs:
            setattr(self, key, kwargs[key])

class TSquareSite:
    def __init__(self, **kwargs):
        '''
        Encapsulates the raw JSON dictionary that represents a site in TSquare.
        Converts a dictionary to attributes of an object for ease of use.
        This constructor should never be called directly; instead, it is called
        by get_sites.
        '''
        for key in kwargs:
            setattr(self, key, kwargs[key])
        
def _get_ticket(username, password):
    # step 1 - get a CAS ticket
    data = { 'username' : username, 'password' : password }
    response = requests.post(BASE_URL_GATECH + 'rest/tickets', data=data)
    if response.status_code == 400:
        raise TSquareAuthException('Username or password incorrect')
    elif not response.status_code == 201:
        raise TSquareAuthException('Received unexpected HTTP code: {}'
                                   .format(response.status_code))
    # black magic to strip the ticket out of the raw html response
    form_split = response.text.split('<form action="')[1].split(' ')[0]
    ticket = form_split.split('tickets/')[1][:-1]
    # step 2 - get a TSquare service ticket
    data = { 'service' : SERVICE }
    response = requests.post(BASE_URL_GATECH + 'rest/tickets/{}'.format(ticket),
                             data=data)
    if response.status_code == 400:
        raise TSquareAuthException('Parameters missing from ST call')
    elif not response.status_code == 200:
        raise TSquareAuthException('Received unexpected HTTP code: {}'
                                   .format(response.status_code))
    service_ticket = response.text
    return (ticket, service_ticket)

def _tsquare_login(service_ticket):
    session = requests.Session()
    # step 3 - redeem the ticket with TSquare and receive authenticated session
    session.get(SERVICE + '?ticket={}'.format(service_ticket))
    return session

    
    