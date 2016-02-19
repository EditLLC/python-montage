

class Query(object):
    def __init__(self, schema):
        self.schema = schema
        self.terms = []

    def _clone(self):
        query = type(self)(self.schema)
        query.terms.extend(copy.deepcopy(self.terms))
        return query

    def get(self, id):
        self.terms.append(['$get', id])
        return self._clone()

    def get_all(self, index=None, *ids):
        value = ids if index is None else [index, ids]
        self.terms.append(['$get_all', value)
        return self._clone()

    def filter(self, **kwargs):
        # TODO
        return self._clone()

    def has_fields(self, *fields):
        self.terms.append(['$has_fields', fields])
        return self._clone()

    def with_fields(self, *fields):
        self.terms.append(['$with_fields', fields])
        return self._clone()

    def order_by(self, field, ordering=None):
        # TODO
        return self._clone()

    def skip(self, num):
        self.terms.append(['$skip', num])
        return self._clone()

    def limit(self, num):
        self.terms.append(['$limit', num])
        return self._clone()

    def slice(self, num):
        self.terms.append(['$slice', num])
        return self._clone()

    def nth(self, num):
        self.terms.append(['$nth', num])
        return self._clone()

    def sample(self, num):
        self.terms.append(['$sample', num])
        return self._clone()

    def pluck(self, *fields):
        self.terms.append(['$pluck', fields])
        return self._clone()

    def without(self, *fields):
        self.terms.append(['$without', fields])
        return self._clone()

    def count(self, value=None):
        if value:
            self.terms.append(['$count', value])
        else:
            self.terms.append(['$count'])
        return self._clone()

    def sum(self, field):
        self.terms.append(['$sum', field])
        return self._clone()

    def avg(self, field):
        self.terms.append(['$avg', field])
        return self._clone()

    def min(self, field):
        self.terms.append(['$min', field])
        return self._clone()

    def max(self, field):
        self.terms.append(['$max', field])
        return self._clone()

    def between(self, _from, _to, index=None):
        value = [_from, _to] if index is None else [_from, _to, index]
        self.terms.append(['$between', value])
        return self._clone()
