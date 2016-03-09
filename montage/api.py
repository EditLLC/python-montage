import mimetypes

__all__ = ('DataAPI', 'FileAPI', 'SchemaAPI')


class DataAPI(object):
    def __init__(self, client):
        self.client = client

    def save(self, *documents):
        endpoint = 'schemas/{0}/save'.format(schema, document_id)

    def get(self, schema, document_id):
        endpoint = 'schemas/{0}/documents/{1}'.format(schema, document_id)
        return self.client.request(endpoint)

    def delete(self, schema, document_id):
        endpoint = 'schemas/{0}/documents/{1}'.format(schema, document_id)
        return self.client.request(endpoint, method='delete')


class FileAPI(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        return self.client.request('files')

    def get(self, file_id):
        return self.client.request('files/{0}'.format(file_id))

    def delete(self, file_id):
        return self.client.request('files/{0}'.format(file_id), method='delete')

    def save(self, *files):
        '''
            Each file is extected to be a tuple of (name, content), where
            content is a file-like object or the contents as a string.

            client.files.save(('foo.txt', open('/path/to/foo.txt')))
            client.files.save(('foo.txt', StringIO('This is foo.txt')))
            client.files.save(('foo.txt', 'This is foo.txt'))
        '''
        file_list = []
        for name, contents in files:
            content_type = mimetypes.guess_type(name)[0]
            file_list.append(('file', (name, contents, content_type)))
        return self.client.request('files', 'post', files=file_list)


class SchemaAPI(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        return self.client.request('schemas')

    def get(self, schema):
        return self.client.request('schemas/{0}'.format(schema))


class UserAPI(object):
    attributes = ('email', 'full_name', 'password')

    def __init__(self, client):
        self.client = client

    def list(self, **kwargs):
        return self.client.request('users', params=kwargs)

    def create(self, full_name, email, password):
        payload = {
            'full_name': full_name,
            'email': email,
            'password': password,
        }
        return self.client.request('users', method='post', json=payload)

    def get(self, user_id):
        return self.client.request('users/{0}'.format(user_id))

    def update(self, user_id, full_name=None, email=None, password=None):
        payload = {}
        if full_name:
            payload['full_name'] = full_name
        if email:
            payload['email'] = email
        if password:
            payload['password'] = password

        return self.client.request('users/{0}'.format(user_id),
            method='patch', json=payload)

    def delete(self, user_id):
        return self.client.request('users/{0}'.format(user_id), method='delete')
