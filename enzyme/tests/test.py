# -*- coding: utf-8 -*-
from enzyme.mkv import MKV, MalformedMKVError
import glob
import io
import logging
import os.path
from pprint import pprint


# logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig()
# for filepath in glob.glob(os.path.expanduser('~/bh_tvshows/*/*/*.mkv')):
for filepath in glob.glob(os.path.expanduser('~/bh_movies/*/*.mkv')):
# for filepath in glob.glob(os.path.expanduser(u'~/Vidéos/*.mkv')):
    print os.path.basename(filepath)
    try:
        m = MKV(io.open(filepath, 'rb'))
        print str(m)
        pprint(m.to_dict())
    except MalformedMKVError:
        print 'Error'
        pass
    print '-' * 100
