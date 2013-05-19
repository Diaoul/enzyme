# -*- coding: utf-8 -*-
__all__ = ['EnzymeException', 'MalformedMKVError', 'ParserError', 'ReadError', 'SizeError']


class EnzymeException(Exception):
    """Base class for enzyme exceptions"""
    pass


class MalformedMKVError(EnzymeException):
    """Wrong or malformed element found"""
    pass


class ParserError(EnzymeException):
    """Base class for exceptions in parsers"""
    pass


class ReadError(ParserError):
    """Unable to correctly read"""
    pass


class SizeError(ParserError):
    """Mismatch between the type of the element and the size of its data"""
    pass
