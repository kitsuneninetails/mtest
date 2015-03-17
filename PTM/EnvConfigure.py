#!/usr/bin/env python
# Copyright 2015 Midokura SARL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

from MTestExceptions import *
from MTestRootServer import RootServer

GlobalConfig = {
    'bridges':
    [
        ('br0', '', [('10.0.0.240', '24')])
    ],
    'zookeeper':
    [
        ('zoo1', 'br0', [('10.0.0.2', '24')]),
        ('zoo2', 'br0', [('10.0.0.3', '24')]),
        ('zoo3', 'br0', [('10.0.0.4', '24')])
    ],
    'cassandra':
    [
        ('cass1', 'br0', [('10.0.0.5', '24')], '56713727820156410577229101238628035242'),
        ('cass2', 'br0', [('10.0.0.6', '24')], '113427455640312821154458202477256070484'),
        ('cass3', 'br0', [('10.0.0.7', '24')], '170141183460469231731687303715884105726')
    ],
    'compute':
    [
        ('cmp1', 'br0', [('10.0.0.8', '24')]),
        ('cmp2', 'br0', [('10.0.0.9', '24')]),
        ('cmp3', 'br0', [('10.0.0.10', '24')])
    ],
    'routers':
    [
        ('quagga',
         [('eth0', ('cmp1', 'eth1'), [('10.0.1.240', '16')]),
          ('eth1', ('cmp2', 'eth1'), [('10.0.2.240', '16')])])
    ],
    'hosted_vms':
    [
    ],
    'vlans':
    [
    ]
}

try:

    if len(sys.argv) < 2:
        print 'Usage: python MTestEnvConfigure {boot|init|start|stop|shutdown|config} [options]'
        raise ExitCleanException()
    else:
        cmd = sys.argv[1]
        
        os_host = RootServer()
        os_host.init_from_python_map(GlobalConfig)
        
        if cmd == 'boot':
            os_host.setup()
        elif cmd == 'init':
            os_host.prepare_files()
        elif cmd == 'start':
            os_host.start()
        elif cmd == 'stop':
            os_host.stop()
        elif cmd == 'shutdown':
            os_host.cleanup()
        elif cmd == 'config':
            os_host.print_config()
        elif cmd == 'control':
            os_host.control(*sys.argv[2:])
        else:
            raise ArgMismatchException(' '.join(sys.argv[1:]))
   
except ExitCleanException:
    exit(1)
except ArgMismatchException as a:
    print 'Argument mismatch: ' + str(a)
    print 'Usage: python MTestEnvConfigure {boot|init|start|stop|shutdown|config} [options]'
    exit(2)
except ObjectNotFoundException:
    exit(2)