import unittest
import tsquare_api

TSQUARE_LOGIN = ''
TSQUARE_PASS = ''

class TSquareAPITests(unittest.TestCase):

    def setUp(self):
        if TSQUARE_LOGIN == '' or TSQUARE_PASS == '':
            self.skipTest('Username or password not supplied.')
    
    def test_login(self):
        api = tsquare_api.TSquareAPI(TSQUARE_LOGIN, TSQUARE_PASS)
        self.assertEqual(api.username, TSQUARE_LOGIN)
        self.assertIsNotNone(api._tg_ticket)
        self.assertIsNotNone(api._service_ticket)
        self.assertIsNotNone(api._session)

    def test_logout(self):
        api = tsquare_api.TSquareAPI(TSQUARE_LOGIN, TSQUARE_PASS)
        self.assertTrue(api._authenticated)
        api.logout()
        self.assertFalse(api._authenticated)


    def test_user_info(self):
        api = tsquare_api.TSquareAPI(TSQUARE_LOGIN, TSQUARE_PASS)
        user = api.get_user_info()
        self.assertIsInstance(user, tsquare_api.TSquareUser)
        self.assertEqual(user.displayId, TSQUARE_LOGIN)
        self.assertTrue(hasattr(user, 'createdTime'))
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'entityURL'))
        self.assertTrue(hasattr(user, 'lastName'))
        self.assertTrue(hasattr(user, 'reference'))
        self.assertTrue(hasattr(user, 'displayId'))
        self.assertTrue(hasattr(user, 'entityId'))
        self.assertTrue(hasattr(user, 'firstName'))
        self.assertTrue(hasattr(user, 'modifiedTime'))
        self.assertTrue(hasattr(user, 'sortName'))
        self.assertTrue(hasattr(user, 'displayName'))
        self.assertTrue(hasattr(user, 'entityReference'))
        self.assertTrue(hasattr(user, 'id'))
        self.assertTrue(hasattr(user, 'owner'))
        self.assertTrue(hasattr(user, 'type'))
        self.assertTrue(hasattr(user, 'eid'))
        self.assertTrue(hasattr(user, 'entityTitle'))
        self.assertTrue(hasattr(user, 'lastModified'))
        self.assertTrue(hasattr(user, 'props'))
        self.assertTrue(hasattr(user, 'url'))

    def test_sites(self):
        api = tsquare_api.TSquareAPI(TSQUARE_LOGIN, TSQUARE_PASS)
        sites = api.get_sites()
        for site in sites:
            self.assertTrue(hasattr(site, 'activeEdit'))
            self.assertTrue(hasattr(site, 'entityReference'))
            self.assertTrue(hasattr(site, 'infoUrl'))
            self.assertTrue(hasattr(site, 'modifiedTime'))
            self.assertTrue(hasattr(site, 'shortDescription'))
            self.assertTrue(hasattr(site, 'createdDate'))
            self.assertTrue(hasattr(site, 'entityTitle'))
            self.assertTrue(hasattr(site, 'infoUrlFull'))
            self.assertTrue(hasattr(site, 'owner'))
            self.assertTrue(hasattr(site, 'siteGroups'))
            self.assertTrue(hasattr(site, 'createdTime'))
            self.assertTrue(hasattr(site, 'entityURL'))
            self.assertTrue(hasattr(site, 'joinable'))
            self.assertTrue(hasattr(site, 'props'))
            self.assertTrue(hasattr(site, 'siteOwner'))
            self.assertTrue(hasattr(site, 'customPageOrdered'))
            self.assertTrue(hasattr(site, 'iconFullUrl'))
            self.assertTrue(hasattr(site, 'joinerRole'))
            self.assertTrue(hasattr(site, 'providerGroupId'))
            self.assertTrue(hasattr(site, 'skin'))
            self.assertTrue(hasattr(site, 'description'))
            self.assertTrue(hasattr(site, 'iconUrl'))
            self.assertTrue(hasattr(site, 'lastModified'))
            self.assertTrue(hasattr(site, 'pubView'))
            self.assertTrue(hasattr(site, 'title'))
            self.assertTrue(hasattr(site, 'empty'))
            self.assertTrue(hasattr(site, 'iconUrlFull'))
            self.assertTrue(hasattr(site, 'maintainRole'))
            self.assertTrue(hasattr(site, 'published'))
            self.assertTrue(hasattr(site, 'type'))
            self.assertTrue(hasattr(site, 'entityId'))
            self.assertTrue(hasattr(site, 'id'))
            self.assertTrue(hasattr(site, 'modifiedDate'))
            self.assertTrue(hasattr(site, 'reference'))
            self.assertTrue(hasattr(site, 'userRoles'))
            self.assertIn('banner-crn', site.props)
            self.assertIn('term', site.props)
            self.assertIn('term_eid', site.props)

    def test_unauth_get_user(self):
        api = tsquare_api.TSquareAPI(TSQUARE_LOGIN, TSQUARE_PASS)
        api._authenticated = False
        with self.assertRaises(tsquare_api.NotAuthenticatedException):
            api.get_user_info()

    def test_unauth_get_sites(self):
        api = tsquare_api.TSquareAPI(TSQUARE_LOGIN, TSQUARE_PASS)
        api._authenticated = False
        with self.assertRaises(tsquare_api.NotAuthenticatedException):
            api.get_sites()

    def test_bad_login(self):
        with self.assertRaises(tsquare_api.TSquareAuthException):
            api = tsquare_api.TSquareAPI('BAD_USERNAME', 'BAD_PASSWORD')

    
        

            