#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import socket
import errno
import fcntl
import os

class client:
    def __init__(self):
        self.id = 1
        self.fsm = {}

    def set_worker(self, worker):
        self.worker = worker

    def client_connect(self):
        
        pass

    def state_start(self):
        print("client_start")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.errno, v:
            erronum = v[0]
            if s == None and erronum == errno.EINTR:
                self.client_start()
        if s == None:
            #transfer to "error" state
            action = self.fsm["error"]
            action()

        fcntl.fcntl(s.fileno(), fcntl.F_SETFL, os.O_NONBLOCK | os.O_RDWR)

    def state_connecting(self):
        print("client_connecting")
        pass

    def state_writing(self):
        print("client_writing")
        pass

    def state_reading(self):
        print("client_reading")
        pass

    def state_error(self):
        print("client_error")
        pass

    def state_end(self):
        pass

    def set_state_machine(self):
        self.fsm["start"] = self.state_start
        self.fsm["connecting"] = self.state_connecting
        self.fsm["writing"] = self.state_writing
        self.fsm["reading"] = self.state_reading
        self.fsm["error"] = self.state_error
        self.fsm["end"] = self.state_end

    def run_state_machine(self):
        state = "start"
        action = self.fsm[state]
        action()