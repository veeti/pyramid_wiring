from pyramid.config import Configurator
from pytest import fixture
from webtest import TestApp
from wiring import Graph, FactoryProvider, injected

from pyramid_wiring.scope import RequestScope

@fixture
def app():
    config = Configurator()
    config.include('pyramid_wiring')

    graph = Graph()
    graph.register_scope(RequestScope, RequestScope())
    class Counter(object):
        def __init__(self):
            self.count = 1
    graph.register_provider('counter', FactoryProvider(Counter, scope=RequestScope))
    config.set_object_graph(graph)

    def count(request, counter=injected('counter')):
        # Increment the counter
        count = counter.count
        counter.count += 1

        # Get the counter from the graph again and make sure it's the same
        assert graph.get('counter') is counter

        return count
    config.add_route('count', '/count')
    config.add_view(count, route_name='count', renderer='string')

    return TestApp(config.make_wsgi_app())

def test_counter_scoped_to_request(app):
    assert app.get('/count').body == b"1"
    assert app.get('/count').body == b"1"
