from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.traversal import DefaultRootFactory
from pytest import fixture, mark
from webtest import TestApp
from wiring import Graph, injected

from pyramid_wiring.mapper import WiringViewMapper

# Function-based views

def view(request):
    assert is_request(request)

    return "Hello, world!"

def context_view(context, request):
    assert is_context(context)
    assert is_request(request)

    return view(request)

def injected_view(request, message=injected('hello')):
    assert is_request(request)

    return message

def context_injected_view(context, request, message=injected('hello')):
    assert is_context(context)
    assert is_request(request)

    return message

# Class-based views

class ClassView(object):

    def __init__(self, request):
        assert is_request(request)

    def __call__(self):
        return "Hello, world!"

class AttributeClassView(ClassView):

    def __call__(self):
        raise AssertionError("Shouldn't get called.")

    def attr(self):
        return "Hello, world!"

class ContextClassView(ClassView):

    def __init__(self, context, request):
        assert is_context(context)
        assert is_request(request)

class InjectedClassView(object):

    def __init__(self, request, message=injected('hello')):
        assert is_request(request)

        self.message = message

    def __call__(self):
        return self.message

class InjectedContextClassView(InjectedClassView):

    def __init__(self, context, request, message=injected('hello')):
        assert is_context(context)
        assert is_request(request)

        self.message = message

@mark.parametrize('view', [
    view,
    context_view,
    injected_view,
    context_injected_view,

    ClassView,
    AttributeClassView,
    ContextClassView,
    InjectedClassView,
    InjectedContextClassView,
])
def test_view_mapping(view):
    config = Configurator()
    config.include('pyramid_wiring')

    # Create a graph with the message.
    graph = Graph()
    graph.register_instance('hello', "Hello, world!")
    config.set_object_graph(graph)

    # Add the view.
    config.add_route('test', '/')
    args = dict(route_name='test', renderer='string')
    if hasattr(view, 'attr'):
        args['attr'] = 'attr'
    config.add_view(view, **args)

    app = TestApp(config.make_wsgi_app())
    assert app.get('/').body == b"Hello, world!"

def is_context(context):
    return isinstance(context, DefaultRootFactory)

def is_request(request):
    return isinstance(request, Request)
