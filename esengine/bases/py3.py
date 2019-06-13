import sys

_IS_PY3 = sys.version_info > (3,)

if _IS_PY3:
    unicode = str
    long = int
    basestring = str
