from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from wiring import Graph, FunctionProvider, FactoryProvider, GraphValidationError, injected
from pytest import fixture

from pyramid_wiring.graph import view_id

@fixture
def graph():
    return Graph()

@fixture
def config(graph):
    config = Configurator()
    config.include('pyramid_wiring')
    config.set_object_graph(graph)
    return config

# Configuration

def test_graph_set_in_registry(graph, config):
    config.commit()
    assert config.registry.graph is graph

def test_configuration_error_without_graph():
    config = Configurator()
    config.include('pyramid_wiring')
    try:
        config.commit()
        raise AssertionError("Expected configuration error.")
    except ConfigurationError as e:
        assert "No object graph" in str(e)

# View graphing

def test_adds_views_to_graph(graph, config):
    def my_view(request):
        pass
    class ClassView(object):
        def __init__(self, request):
            pass
    config.add_route('root', '/')
    config.add_route('hello', '/hello')
    config.add_view(my_view, route_name='root')
    config.add_view(ClassView, route_name='hello')

    config.commit()

    assert view_id(my_view) in graph.providers
    assert view_id(ClassView) in graph.providers
    assert isinstance(graph.providers[view_id(my_view)], FunctionProvider)
    assert isinstance(graph.providers[view_id(ClassView)], FactoryProvider)

def test_graph_is_validated(config):
    def my_view(request, dependency=injected('not in graph')):
        pass
    config.add_route('root', '/')
    config.add_view(my_view, route_name='root')

    try:
        config.commit()
        raise AssertionError("Expected validation error.")
    except ConfigurationError as err:
        assert isinstance(err.evalue, GraphValidationError)

# Other

def test_id_generation():
    def my_view(request):
        pass
    class MyView(object):
        pass
    assert 'my_view' in view_id(my_view)
    assert 'MyView' in view_id(MyView)
