Python Thrift client wrapper
============================

Tired of managing Thrift TTransport's and Clients?  Wrap them into one
thriftclient.Client.  Calls made to the client that are not open or
close will be passed to the underlying client.

Usage
-----

    >>> import sys
    >>> sys.path('../gen-py')
    >>> from tutorial import Caclulator
    >>> from tutorial.ttypes import *
    >>> import thriftclient
    >>> c = thriftclient.Client("localhost", 9090, Calculator, framed=False)
    >>> c.ping()
    >>> c.add(1, 1)
    2
    >>> c.close()
    >>> c.open()
    >>> c.add(2, 3)
    5
    >>> c.close()
    >>>
