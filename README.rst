==============
pyramid_wiring
==============

A library for using the wiring_ dependency injection library with the Pyramid_ web framework. ``pyramid_wiring`` injects views and provides a request scope for dependencies.

Setup
=====

Include ``pyramid_wiring`` in your configuration:

::

    config.include('pyramid_wiring')

Create the object graph with all your dependencies and pass it to the ``Configurator``:

::

    graph = Graph()
    ...
    config.set_object_graph(graph)

``pyramid_wiring`` will validate and add all of your views to the graph during configuration and set a default `view mapper`_ that injects requested dependencies.

To make sure the ``WiringViewMapper`` is applied to all of your views, include ``pyramid_wiring`` before adding any views.

Usage
=====

See the wiring_ documentation. Your views can request dependencies as usual - for example, in a view function:

::

    from wiring import injected

    @view_config(route_name='users', request_method='GET')
    def users(request, dao=injected('user_dao')):
        return dao.get_users()

Or a class-based view:

::

    class UserView(object):

        def __init__(self, request, dao=injected('user_dao')):
            self.request = request
            self.dao = dao

        @view_config(route_name='users', request_method='GET')
        def users(self):
            return self.dao.get_users()

You can also get the graph directly from the application registry if needed:

::

    def view(request):
        graph = request.registry.graph
        # do something

A new ``RequestScope`` is also included:

::

    from pyramid_wiring import RequestScope

    graph.register_scope(RequestScope, RequestScope())
    graph.register_factory('database', Database, scope=RequestScope)

License
=======

See ``LICENSE``.

.. _wiring: https://wiring.readthedocs.org/en/latest/
.. _Pyramid: http://www.pylonsproject.org/
.. _view mapper: http://docs.pylonsproject.org/projects/pyramid/en/1.5-branch/narr/hooks.html#using-a-view-mapper
