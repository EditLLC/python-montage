==============
python-montage
==============

.. image:: https://circleci.com/gh/EditLLC/python-montage/tree/feature%2fv2.svg?style=shield
   :target: https://circleci.com/gh/EditLLC/python-montage/tree/feature%2fv2
   :alt: CircleCI

.. image:: https://codecov.io/github/EditLLC/python-montage/coverage.svg?branch=feature/v2
   :target: https://codecov.io/github/EditLLC/python-montage?branch=feature/v2
   :alt: Coverage

Python library for Montage

Usage
=====

::

    >>> import montage
    >>> client = montage.Client(subdomain[, token])
    >>> client.authenticate(email, password)  # sets client.token

    # Current user
    >>> client.user()

    # Querying and scripting
    >>> query = montage.Query('schema')
    >>> query = query.filter(**kwargs)
    >>> query = query.limit(10)
    >>> query = query.skip(10)
    >>> query = query.order_by(field[, ordering=asc|desc])

    >>> script = montage.Script('foobar.lua')

    >>> evaluated = montage.RunLua('''
    ...     function max(num1, num2)
    ...
    ...        if (num1 > num2) then
    ...           result = num1;
    ...        else
    ...           result = num2;
    ...        end
    ...
    ...        return result;
    ...     end
    ...
    ...     return max(10, 4)
    ... ''')

    >>> client.run(query=query, foobar=script, max=evaluated)
    {
        "data": {
            "query": [ ... ],
            "foobar": " ... ",
            "max": 10,
        }
    }

    # Schemas
    >>> client.schemas.list()
    >>> client.schemas.get('schema')

    # Data
    >>> client.data.save(schema, *documents)
    >>> client.data.get(schema, document_id)
    >>> client.data.delete(schema, document_id)

    # Files
    >>> client.files.list()
    >>> client.files.save(*files)
    >>> client.files.get(file_id)
    >>> client.files.delete(file_id)

    # Users
    >>> client.users.list()
    >>> client.users.list(email__endswith='gmail.com')
    >>> client.users.create(
    ...     full_name='Test User',
    ...     email='test@example.com',
    ...     password='letmein'
    ... )
    >>> client.users.get(user_id)
    >>> client.users.update(user_id, password='changeme')
    >>> client.users.delete(user_id)
