import mimetypes
import os

from cached_property import cached_property

from . import api
from .compat import urljoin
from .requestor import APIRequestor

__all__ = ('Client', 'client')


class Client(object):
    host = 'mntge.com'
    protocol = 'https'
    timeout = 10

    def __init__(self, project, token=None):
        self.project = project
        self.token = token
        self.requestor = APIRequestor(self)

    @property
    def domain(self):
        return '{0}.{1}'.format(self.project, self.host)

    def request(self, endpoint, method=None, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        return self.requestor.request(self.url(endpoint), method, **kwargs)

    def url(self, endpoint):
        return '{protocol}://{domain}/api/v1/{endpoint}/'.format(
            protocol=self.protocol,
            domain=self.domain,
            endpoint=endpoint,
        )

    def authenticate(self, email, password):
        response = self.request('user', method='post', data={
            'username': email,
            'password': password
        })
        self.token = response.get('data', {}).get('token')
        if self.token is None:
            return False
        return True

    def user(self):
        if self.token:
            return self.request('user')

    def execute(self, **kwargs):
        queryset = {key: executable.as_dict()
            for key, executable in kwargs.items()}
        return self.request('execute', method='post', json=queryset)

    @cached_property
    def documents(self):
        return api.DocumentsAPI(self)

    @cached_property
    def files(self):
        return api.FileAPI(self)

    @cached_property
    def roles(self):
        return api.RoleAPI(self)

    @cached_property
    def schemas(self):
        return api.SchemaAPI(self)

    @cached_property
    def users(self):
        return api.UserAPI(self)

    @cached_property
    def policies(self):
        return api.PolicyAPI(self)

    @cached_property
    def tasks(self):
        return api.TaskAPI(self)


client = Client(
    project=os.environ.get('MONTAGE_PROJECT'),
    token=os.environ.get('MONTAGE_TOKEN')
)
