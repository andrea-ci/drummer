import pathchange
pathchange.fix()

from core.sockets.server import SocketServer

ss = SocketServer(None)
ss.run()
