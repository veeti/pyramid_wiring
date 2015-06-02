from .scope import RequestScope
from .mapper import WiringViewMapper
from .graph import view_id

def includeme(config):
    config.include('.graph')
    config.include('.mapper')
