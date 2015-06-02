import inspect

from wiring import FunctionProvider

from .graph import view_id

class WiringViewMapper(object):
    """
    A view mapper that uses the application's wiring graph to inject view
    callables.
    """

    def __init__(self, **args):
        self.graph = args['registry'].graph
        self.attr = args.get('attr')

    def __call__(self, view):
        def wrapper(context, request):
            name = view_id(view)
            provider = self.graph.providers[name]

            args = [request]

            # Figure out what arguments the view takes: context and request,
            # or just the request?
            if inspect.isclass(view):
                spec = inspect.getargspec(view.__init__).args[1:]
            else:
                spec = inspect.getargspec(view).args
            if len(spec) - len(provider.dependencies) > 1:
                args.insert(0, context)

            if inspect.isclass(view):
                target = self.graph.get(name, *args)
                if self.attr:
                    target = getattr(target, self.attr)
                return target()
            else:
                return self.graph.get(name)(*args)
        return wrapper


def includeme(config):
    config.set_view_mapper(WiringViewMapper)
