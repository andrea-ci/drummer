#!/usr/bin/python3
# -*- coding: utf-8 -*-
from multiprocessing import Process, Pipe
from workers.socketserver import SocketServer

def sender(conn, msgs):
    """ function to send messages to other end of pipe """
    
    for msg in msgs:
        conn.send(msg)
        print("Sent the message: {}".format(msg))
        conn.close()


class Sender(Process):

    def __init__(self, conn, msgs):

        super().__init__()

        self.conn = conn
        self.msgs = msgs


    def run(self):

        for msg in self.msgs:
            self.conn.send(msg)
            print("Sent the message: {}".format(msg))

        self.conn.close()


def receiver(conn):

    while 1:
        msg = conn.recv()
        if msg == "END":
            break
        print("Received the message: {}".format(msg))


if __name__ == "__main__":

    # messages to be sent
    msgs = ["hello", "hey", "hru?", "END"]

    # creating a pipe
    parent_conn, child_conn = Pipe()

    # creating new processes
    #p1 = Process(target=sender, args=(parent_conn,msgs))
    p1 = Sender(parent_conn,msgs)
    p2 = Process(target=receiver, args=(child_conn,))
    p3 = SocketServer()

    # running processes
    p1.start()
    p2.start()
    p3.start()

    # wait until processes finish
    p1.join()
    p2.join()
    p3.join()
