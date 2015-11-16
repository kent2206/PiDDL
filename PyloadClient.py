import json
import urllib
import urllib2


class PyloadClient:
    def __init__(self, HOST, PORT, USER, PASSWORD):
        self.HOST = HOST
        self.PORT = PORT
        self.USER = USER
        self.PASSWORD = PASSWORD

        self.json_encoder = json.JSONEncoder()

        self.base_url = 'http://%s:%s/api/' % (HOST, PORT)
        self.SESSION_ID = self.login()

    def __call(self, function, **params):
        u = 'http://%s:%s/api/%s' % (self.HOST, self.PORT, function)

        if function is not 'login':
            params['session'] = self.SESSION_ID
        post_data = urllib.urlencode(params)

        print u, post_data
        rep = urllib2.urlopen(u, post_data).read()
        print rep
        return json.loads(rep)

    def login(self):
        return self.__call('login', username=self.USER, password=self.PASSWORD)

    def get_server_version(self):
        return self.__call('getServerVersion')