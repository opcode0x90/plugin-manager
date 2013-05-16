"""
Minimalistic plugin manager for Python

Requires:
  zope.interface

by:
  opcode0x90, 15 May 2013
"""
import importlib
from zope.interface import Attribute


###############################################################################

def get_class(classname, interface=None):
    """
    Locate the specified class by name, optionally verify that it implements
    specified interface
    """
    modname, _, clsname = classname.rpartition('.')

    module = importlib.import_module(modname)
    class_ = getattr(module, clsname)

    if interface and not interface.implementedBy(class_):
        # wrong interface
        raise ImportError("'%s' does not implement interface '%s'"
                         % (classname, interface))

    return class_


def get_attributes(cls):
    """
    Introspect the specified class and extract all exported attributes
    """
    return [x for x in dir(cls) if getattr(cls, x).__class__ is Attribute]


def construct(cls, params=dict()):
    """
    Construct the specified class with given params
    """
    obj = cls()
    for attr, value in params.iteritems():
        if hasattr(obj, attr):
            setattr(obj, attr, value)
    return obj


def load_class(classname, params=dict(), interface=None):
    """
    Convinience wrapper for both get_class() and construct()
    """
    cls = get_class(classname, interface)
    return construct(cls, params)


def load_classes(classlist, interface=None):
    """
    Convinience method for loading multiple classes from list
    """
    def _load_class(t):
        if isinstance(t, tuple):
            classname, params = t
        else:
            classname = t
            params = dict()

        return (classname, load_class(classname, params, interface))

    return [_load_class(t) for t in classlist]


def load_modules(modulelist):
    """
    Convinience method for loading list of modules
    """
    return [importlib.import_module(m) for m in modulelist]

###############################################################################
