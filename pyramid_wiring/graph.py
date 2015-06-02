import inspect

from pyramid.exceptions import ConfigurationError
from wiring import FactoryProvider, FunctionProvider

def view_id(view):
    """
    Creates a unique identifier for the specified view callable.
    """
    return "pyramid_wiring.{id!s}.{name}".format(id=id(view), name=getattr(view, '__name__'))

def prepare_graph(config, done=False):
    """
    Prepares the object graph in the configuration.
    """
    if not hasattr(config.registry, 'graph'):
        raise ConfigurationError("No object graph set in the Configurator. Provide one with set_object_graph.")
    graph = config.registry.graph
    graph_views(config, graph)
    graph.validate()

def set_object_graph(config, graph):
    """
    Prepares to set the specified graph in the configuration.
    """
    def action():
        config.registry.graph = graph
    config.action('set_object_graph', callable=action)

def graph_views(config, graph):
    """
    Registers every view in the configuration to the graph.
    """
    for view in config.registry.introspector.get_category('views'):
        view = view['introspectable']['callable']
        name = view_id(view)
        if name in graph.providers:
            continue

        if inspect.isclass(view):
            provider = FactoryProvider(view)
        else:
            provider = FunctionProvider(view)
        graph.register_provider(name, provider)

def includeme(config):
    config.add_directive('set_object_graph', set_object_graph)
    config.action('prepare_graph', callable=prepare_graph, args=(config,), order=9001)
