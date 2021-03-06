from jsonrpc import ServiceProxy

class Controller(object):
    '''
    A connector to a bitcoin daemon. A caching is done so that if the args are the same
    than a previous call to Controller(...), the previous instance is reused.
    A call to Controller() without any arguments tries to reuse an arbitrary instance
    that is already cached, if any. This is particularly useful if you only care about
    one instance of the connector.
    '''

    cache = {}

    def __new__(cls, user='', password='', host='127.0.0.1', port=8332, protocol='http'):
        if ('' == user) and (0 != len(cls.cache)):
            url = cls.cache.keys()[0]
        else:
            url = "%s://%s:%s@%s:%s" % (protocol, user, password, host, port)
            if not url in cls.cache:
                cls.cache[url] = object.__new__(cls)
                cls.cache[url].conn = ServiceProxy(url)
                cls.cache[url].backupwallet = cls.cache[url].conn.backupwallet
                cls.cache[url].getaccountaddress = cls.cache[url].conn.getaccountaddress
                cls.cache[url].getaddressesbyaccount = cls.cache[url].conn.getaddressesbyaccount
                cls.cache[url].getbalance = cls.cache[url].conn.getbalance
                cls.cache[url].getblockcount = cls.cache[url].conn.getblockcount
                cls.cache[url].getblocknumber = cls.cache[url].conn.getblocknumber
                cls.cache[url].getconnectioncount = cls.cache[url].conn.getconnectioncount
                cls.cache[url].getdifficulty = cls.cache[url].conn.getdifficulty
                cls.cache[url].getgenerate = cls.cache[url].conn.getgenerate
                cls.cache[url].setgenerate = cls.cache[url].conn.setgenerate
                cls.cache[url].gethashespersec = cls.cache[url].conn.gehashespersec
                cls.cache[url].getinfo = cls.cache[url].conn.getinfo
                cls.cache[url].getaccount = cls.cache[url].conn.getaccount
                cls.cache[url].gettransaction = cls.cache[url].conn.gettransaction
                cls.cache[url].setaccount = cls.cache[url].conn.setaccount
                cls.cache[url].getnewaddress = cls.cache[url].conn.getnewaddress
                cls.cache[url].getreceivedbyaddress = cls.cache[url].conn.getreceivedbyaddress
                cls.cache[url].getreceivedbyaccount = cls.cache[url].conn.getreceivedbyaccount
                cls.cache[url].help = cls.cache[url].conn.help
                cls.cache[url]._listreceivedbyaddress = cls.cache[url].conn.listreceivedbyaddress
                cls.cache[url]._listreceivedbyaccount = cls.cache[url].conn.listreceivedbyaccount
                cls.cache[url].listtransactions = cls.cache[url].conn.listtransactions
                cls.cache[url].move = cls.cache[url].conn.move
                cls.cache[url].sendfrom = cls.cache[url].conn.sendfrom
                cls.cache[url].sendtoaddress = cls.cache[url].conn.sendtoaddress
                cls.cache[url].getwork = cls.cache[url].conn.getwork
                cls.cache[url].stop = cls.cache[url].conn.stop
                cls.cache[url].validateaddress = cls.cache[url].conn.validateaddress
        return cls.cache[url]

    def listreceivedbyaddress(self, info=None):
        '''An enhanced version of standard listreceivedbyaddress. It accepts
           an optional secondary argument, 'info', that makes the function
           return a simple dict (address as key, info as value). 'info' can
           be 'amount', 'account'/'label', 'confirmations'.'''
        l = self._listreceivedbyaddress()
        if info is None:
            return l
        else:
            return dict([[l[i]['address'], l[i][info]] for i in range(len(l))])

    def listreceivedbyaccount(self, info=None):
        '''Same as listreceivedbyaddress(), with accounts.
           'info' can be 'amount' or 'confirmations' (it can also be 'label',
           but that would be pointless).'''
        l = self._listreceivedbyaccount()
        if info is None:
            return l
        else:
            return dict([[l[i]['account'], l[i][info]] for i in range(len(l))])

class BitcoinServerIOError(IOError):
    '''There was a problem when connecting to the bitcoin server'''
    pass
