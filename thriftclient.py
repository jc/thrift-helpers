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
    def __init__(self, host, port, service, framed=True, timeout=50000):
        """Creates a new thrift client.

        host - host of server.
        port - port of server.
        service - the class the server implements
        framed - should this client be framed? (for non-blocking clients)
        timeout - timeout in ms
        """
        self.host = host
        self.port = port
        self.service = service
        self.framed = framed
        self.timeout = timeout
        self.create()

    def create(self):
        self.transport = None
        try:
            transport = TSocket.TSocket(self.host, self.port)
            transport.setTimeout(self.timeout)
            if self.framed:
                transport = TTransport.TFramedTransport(transport)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = self.service.Client(protocol)
            transport.open()
        except Thrift.TException, tx:
            print 'Exception in creating client: %s' % (tx.message)
            raise tx
        self.transport = transport
        self.client = client

    def recreate(self):
        self.close()
        self.create()
        
    def close(self):
        """Close the socket when you are done!"""
        if self.transport.isOpen():
            self.transport.close()

    def open(self):
        """Open a socket."""
        if self.transport.isOpen():
            self.transport.close();
        try:
            self.transport.open()
        except Thrift.TException, tx:
            print 'Cannot open Client: %s' % (tx.message)
            raise tx

    def __getattr__(self, attr):
        if attr.startswith('_'):
            raise AttributeError("No such attribute '%s'" % attr)
        return self.client.__getattribute__(attr)

    
