from pyramid.threadlocal import get_current_request
from wiring import interface
from wiring.scopes import IScope

@interface.implements(IScope)
class RequestScope(object):
    """
    A wiring scope where provided instances are cached per request.
    """

    def _get(self):
        request = get_current_request()
        if not hasattr(request, '_wiring_scope'):
            request._wiring_scope = {}
        return request._wiring_scope

    def __getitem__(self, specification):
        return self._get().__getitem__(specification)

    def __setitem__(self, specification, instance):
        return self._get().__setitem__(specification, instance)

    def __contains__(self, specification):
        return self._get().__contains__(specification)
