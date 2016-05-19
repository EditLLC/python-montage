import copy
import datetime

__all__ = ('Query',)


class Field(object):
    modifiers = ('date', 'time', 'year', 'month', 'day', 'hours', 'minutes',
        'seconds', 'day_of_month', 'day_of_year', 'timezone')
    operators = ('eq', 'ne', 'lt', 'le', 'gt', 'ge', 'ieq', 'in', 'contains',
        'regex', 'starts', 'istarts', 'ends', 'iends', 'intersects', 'includes')

    def __init__(self, field):
        self.field = field

    def __eq__(self, other):
        return self.eq(other)

    def __ne__(self, other):
        return self.ne(other)

    def __lt__(self, other):
        return self.lt(other)

    def __le__(self, other):
        return self.le(other)

    def __gt__(self, other):
        return self.gt(other)

    def __ge__(self, other):
        return self.ge(other)

    def in_(self, value):
        return getattr(self, 'in')(value)

    def __getattr__(self, attr):
        if attr in self.operators:
            return self._operator(attr)
        if attr in self.modifiers:
            return self._modifier(attr)
        raise AttributeError("'row' object has no attribute '{0}'".format(attr))

    def _modifier(self, modifier):
        def inner():
            return Field('{0}.${1}'.format(self.field, modifier))
        return inner

    def _operator(self, operator):
        def inner(value):
            return [self.field, ['${0}'.format(operator), self._coerce(value)]]
        return inner

    def _coerce(self, value):
        if isinstance(value, datetime.datetime):
            return ['$datetime', str(value)]
        if isinstance(value, datetime.date):
            return ['$date', str(value)]
        if isinstance(value, datetime.time):
            return ['$time', str(value)]
        return value


class Query(object):
    def __init__(self, schema):
        self.schema = schema
        self.terms = []

    @classmethod
    def AND(cls, *args):
        return ['$and', args]

    @classmethod
    def OR(cls, *args):
        return ['$or', args]

    @classmethod
    def NOT(cls, *args):
        return ['$not', args]

    def _append(self, term, **kwargs):
        if kwargs:
            self.terms.append([term, kwargs])
        else:
            self.terms.append([term])
        return self._clone()

    def _clone(self):
        query = type(self)(self.schema)
        query.terms.extend(copy.deepcopy(self.terms))
        return query

    def as_dict(self):
        return {
            '$type': 'query',
            '$schema': self.schema,
            '$query': copy.deepcopy(self.terms)
        }

    # Selecting data

    def get(self, id):
        return self._append('$get', key=id)

    def get_all(self, *keys, **kwargs):
        params = {'keys': keys}
        if 'index' in kwargs:
            params['index'] = kwargs['index']
        return self._append('$get_all', **params)

    def filter(self, *filters):
        return self._append('$filter', predicate=filters)

    def between(self, lower_key='$min', upper_key='$max', **kwargs):
        return self._append('$between', lower_key=lower_key, upper_key=upper_key, **kwargs)

    # Transformations

    def has_fields(self, *fields):
        return self._append('$has_fields', fields=fields)

    def with_fields(self, *fields):
        return self._append('$with_fields', fields=fields)

    def order_by(self, key=None, index=None, ordering=None):
        params = {}
        if key is not None:
            params['key'] = key
        if index is not None:
            params['index'] = index
        if ordering is not None:
            try:
                params['ordering'] = {
                    'asc': '$asc',
                    'desc': '$desc',
                }[ordering]
            except KeyError:
                raise ValueError('ordering must be "asc" or "desc".')
        return self._append('$order_by', **params)

    def skip(self, n):
        return self._append('$skip', n=n)

    def limit(self, n):
        return self._append('$limit', n=n)

    def slice(self, start_offset, end_offset=None, **kwargs):
        if end_offset is not None:
            kwargs['end_offset'] = end_offset
        return self._append('$slice', start_offset=start_offset, **kwargs)

    def nth(self, n):
        return self._append('$nth', n=n)

    def sample(self, n):
        return self._append('$sample', n=n)

    # Manipulation

    def pluck(self, *fields):
        return self._append('$pluck', fields=fields)

    def without(self, *fields):
        return self._append('$without', fields=fields)

    # Aggregation

    def group(self, **kwargs):
        return self._append('$group', **kwargs)

    def count(self):
        return self._append('$count')

    def sum(self, field):
        return self._append('$sum', field=field)

    def avg(self, field):
        return self._append('$avg', field=field)

    def min(self, field):
        return self._append('$min', field=field)

    def max(self, field):
        return self._append('$max', field=field)

    # Geospatial

    def get_intersecting(self, geometry, index):
        return self._append('$get_intersecting', geometry=geometry, index=index)

    def get_nearest(self, geometry, index, **kwargs):
        return self._append('$get_nearest', geometry=geometry, index=index, **kwargs)

