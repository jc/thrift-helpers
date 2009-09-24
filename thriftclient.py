from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class Client:
    """thriftclient.Client provides a simple wrapper around a Thrift
    service.  This removes need to maintain a client and transport
    object.  Undefined calls to the Client are mapped to the underlying
    client.

    
    """
    def __init__(self, host, port, service, framed=True):
        """Creates a new thrift client.

        host - host of server.
        port - port of server.
        service - the class the server implements
        framed - should this client be framed? (for non-blocking clients)
        """
        self.transport = None
        try:
            transport = TSocket.TSocket(host, port)
            if framed:
                transport = TTransport.TFramedTransport(transport)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = service.Client(protocol)
            transport.open()
        except Thrift.TException, tx:
            print 'Exception in creating client: %s' % (tx.message)
            raise tx
        self.transport = transport
        self.client = client
        
    def close(self):
        """Close the socket when you are done!"""
        self.transport.close()

    def open(self):
        """Open a socket."""
        try:
            self.transport.open()
        except Thrift.TException, tx:
            print 'Cannot open Client: %s' % (tx.message)
            raise tx

    def __getattr__(self, attr):
        if attr.startswith('_'):
            raise AttributeError("No such attribute '%s'" % attr)
        return self.client.__getattribute__(attr)
    
