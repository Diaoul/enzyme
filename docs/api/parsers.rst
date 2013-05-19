Parsers
=======
A parser extract structured information as a tree from a container as a file-like object.
It does the type conversion when explicit but does not interpret anything else.
Parsers can raise a :class:`~enzyme.exceptions.ParserError`.

.. _ebml:

EBML
----
.. module:: enzyme.parsers.ebml

`EBML (Extensible Binary Meta Language) <http://matroska.org/technical/specs/index.html>`_ is used
by `Matroska <http://en.wikipedia.org/wiki/Matroska>`_ and `WebM <http://en.wikipedia.org/wiki/WebM>`_.

Element types
~~~~~~~~~~~~~
.. data:: INTEGER

    Signed integer element type

.. data:: UINTEGER

    Unsigned integer element type

.. data:: FLOAT

    Float element type

.. data:: STRING

    ASCII-encoded string element type

.. data:: UNICODE

    UTF-8-encoded string element type

.. data:: DATE

    Date element type

.. data:: BINARY

    Binary element type

.. data:: MASTER

    Container element type

Main interface
~~~~~~~~~~~~~~
.. data:: SPEC_TYPES

    :ref:`Specification <specs>` types to `Element types`_ mapping

.. data:: READERS

    `Element types`_ to reader functions mapping. See `Readers`_

    You can override a reader to use one of your choice here::

        >>> def my_binary_reader(stream, size):
        ...     data = stream.read(size)
        ...     return data
        >>> READERS[BINARY] = my_binary_reader 

.. autoclass:: Element
    :members:

.. autoclass:: MasterElement
    :members:

.. autofunction:: parse

.. autofunction:: parse_element

.. autofunction:: get_matroska_specs

Readers
~~~~~~~
.. automodule:: enzyme.parsers.ebml.readers
    :members:

.. _specs:

Specifications
~~~~~~~~~~~~~~
The XML specification for Matroska can be found `here <http://matroska.svn.sourceforge.net/viewvc/matroska/trunk/foundation_src/spectool/specdata.xml>`_.
It is included with enzyme and can be converted to the appropriate format with :func:`~enzyme.parsers.ebml.get_matroska_specs`.

The appropriate format of the `specs` parameter for :func:`~enzyme.parsers.ebml.parse`, :func:`~enzyme.parsers.ebml.parse_element`
and :meth:`~enzyme.parsers.ebml.MasterElement.load` is ``{id: (type, name, level)}``
