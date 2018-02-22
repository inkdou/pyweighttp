#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import threading
from client import client

class worker:
    def __init__(self, config, id, num_clients, num_requests):
        self.id = id
        self.req = None
        self.config = config
        self.clients = [] #new
        self.num_clients = num_clients
        self.progress_interval = num_requests / 10;

        if self.progress_interval == 0:
            self.progress_interval = 1

        for i in range(num_clients):
            self.clients.append(client())

    def work_thread(self):
        print(self.id)