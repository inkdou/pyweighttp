#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import sys
import getopt
import threading

from worker import worker

class Weighttp:
    def __init__(self):
        self.req_count = 1
        self.thread_count = 2
        self.concur_count = 1
        self.req_count = 1
        self.keep_alive = 1
        self.headers = []

    def forge_request(self, args):
        url = args[0]
        if url[:7] == "http://":
            url = url[7:]
        elif url[:8] == "https://":
            url = url[8:]

        arra = url.split(":")
        if len(arra) > 1: #found host:port
            self.host = arra[0]
            arra1 = arra[1].split("/")
            if len(arra1) > 1:
                self.port = int(arra1[0])
                self.url = arra1[1]
            else:
                self.port = int(arra1[0])
        else:
            arra1 = arra[0].split("/")
            self.host = arra1[0]
            self.port = 80
            self.url = arra1[1]

        self.url = "/" + self.url
        header_host = 0
        have_useragent = 0
        for i in range(len(self.headers)):
            strs = self.headers[i]
            if strs[:5] == "Host:":
                if header_host == 1:
                    print("Duplicate Host Header")
                self.header_host = strs
                header_host = 1

            if strs[:11] == "User-Agent:":
                have_useragent = 1
                self.user_agent = strs

        if header_host == 0:
            self.header_host = self.host + self.port
        if have_useragent == 0:
            self.user_agent = "weighttp/1.0"

        self.req = "GET " + self.url + " HTTP/1.1\r\n" + self.header_host + "\r\n" + self.user_agent + "\r\n"

        for i in range(len(self.headers)):
            strs = self.headers[i]
            if strs[:11] == "User-Agent:" or strs[:5] == "Host:":
                continue
            self.req = self.req + strs + "\r\n"

        if self.keep_alive == 1:
            self.req = self.req + "Connection: keep-alive\r\n\r\n"
        else:
            self.req = self.req + "Connection: close\r\n\r\n"

    def Wgetopt(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], ":hv6kn:t:c:H:")
            for o, a in opts:
                if o == "-h":
                    self.show_help()
                    return 0
                if o == "-v":
                    return 0
                if o == "-6":
                    use_ipv6 = 1
                if o == "-k":
                    self.keep_alive = 1
                if o == "-n":
                    self.req_count = int(a)
                if o == "-t":
                    self.thread_count = int(a)
                if o == "-c":
                    self.concur_count = int(a)
                if o == "-H":
                    self.headers.append(a)
            if self.thread_count <= 0:
                self.show_help()
                return 1

            if self.concur_count <= 0:
                self.show_help()
                return 1

            if self.req_count <= 0:
                self.show_help()
                return 1
            if self.req_count == sys.maxint or self.thread_count > self.req_count:
                self.show_help()
                return 1

            self.forge_request(args)
        except getopt.GetoptError:
            print("opt error")


    def run(self):
        self.Wgetopt()
        print("-->request: \n%s") % self.req
        print("-->host: \n%s") % self.header_host
        print("-->port: \n%s") % self.port

        rest_concur = self.concur_count % self.thread_count
        rest_req = self.req_count % self.thread_count

        for i in range(self.thread_count):
            reqs = self.req_count / self.thread_count
            concur = self.concur_count / self.thread_count

            if rest_concur:
                concur += 1
                rest_concur -= 1

            if rest_req:
                reqs += 1
                rest_req -= 1

            worker_t = worker(self, i, concur, reqs)

            threading.Thread(target=worker_t.work_thread(), args=worker_t, name="thread-" + str(worker_t.id))

    def show_help(self):
        print("weighttp <options> <url> \n")
        print(" -n num number of requests (mandatory)\n")
        print(" -t num threadcount        (default:1)\n")
        print(" -c num concurrent clients (default:1)\n")
        print(" -k keepalive              (default:no)")
        print(" -6 use ipv6               (default:no)\n")
        print(" -H str add header to request \n")
        print(" -h show help and exit\n")
        print(" -v show version and exit\n\n")
        print("example: weihttpd -n 10000 -c 10 -t 2 -k -H \"User-Agent: foo\" Location/index.html\n\n")

t = Weighttp()
t.run()