# -*- coding: utf-8 -*-
__title__ = 'enzyme'
__version__ = '0.3.1'
__author__ = 'Antoine Bertin'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2013 Antoine Bertin'


from .mkv import *
import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
from .exceptions import *

logging.getLogger(__name__).addHandler(NullHandler())
