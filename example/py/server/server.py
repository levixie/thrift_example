#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#
from ..tutorial import Calculator
from ..tutorial.ttypes import *
from ..shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.server import TNonblockingServer
import logging
import sys


class CalculatorHandler:
    def __init__(self):
        self.log = {}

    def ping(self):
        logging.info('ping()')

    def add(self, n1, n2):
        logging.info('add(%d,%d)' % (n1, n2))
        return n1 + n2

    def calculate(self, logid, work):
        print 'calculate(%d, %r)' % (logid, work)

        if work.op == Operation.ADD:
            val = work.num1 + work.num2
        elif work.op == Operation.SUBTRACT:
            val = work.num1 - work.num2
        elif work.op == Operation.MULTIPLY:
            val = work.num1 * work.num2
        elif work.op == Operation.DIVIDE:
            if work.num2 == 0:
                x = InvalidOperation()
                x.whatOp = work.op
                x.why = 'Cannot divide by 0'
                raise x
            val = work.num1 / work.num2
        else:
            x = InvalidOperation()
            x.whatOp = work.op
            x.why = 'Invalid operation'
            raise x

        log = SharedStruct()
        log.key = logid
        log.value = '%d' % (val)
        self.log[logid] = log

        return val

    def getStruct(self, key):
        print 'getStruct(%d)' % (key)
        return self.log[key]

    def zip(self):
        print 'zip()'


handler = CalculatorHandler()
processor = Calculator.Processor(handler)
transport = TSocket.TServerSocket(port=9090)
tfactory = TBinaryProtocol.TBinaryProtocolFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

port = 9090

server = TNonblockingServer.TNonblockingServer(processor, transport, tfactory, pfactory)
# log to stdout
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(1)

ch.setFormatter(formatter)
log.addHandler(ch)


# server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# You could do one of these for a multithreaded server
# server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
# server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
