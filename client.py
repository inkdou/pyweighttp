#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

class client:
    def __init__(self):
        self.id = 1
        self.fsm = {}

    def set_worker(self, worker):
        self.worker = worker

    def client_start(self):
        print("client_start")
        pass

    def client_connecting(self):
        print("client_connecting")
        pass

    def client_writing(self):
        print("client_writing")
        pass

    def client_reading(self):
        print("client_reading")
        pass

    def client_error(self):
        print("client_error")
        pass

    def client_end(self):
        pass

    def set_state_machine(self):
        self.fsm["start"] = self.client_start
        self.fsm["connecting"] = self.client_connecting
        self.fsm["writing"] = self.client_writing
        self.fsm["reading"] = self.client_reading
        self.fsm["error"] = self.client_error
        self.fsm["end"] = self.client_end

    def run_state_machine(self):
        state = "start"
        action = self.fsm[state]
        action()