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

from MTestNetworkObject import NetworkObject
from MTestCLI import LinuxCLI

class Interface(NetworkObject):
    def __init__(self, name, near_host):
        super(Interface, self).__init__(name, near_host.get_cli())
        self.near_host = near_host
        self.ip_list = []

    def setup(self):
        self.get_cli().cmd('ip link add dev ' + self.get_name())
        for ip in self.ip_list:
            self.get_cli().cmd('ip addr add ' + ip[0] + '/' + ip[1] + ' dev '  + self.get_name())

    def cleanup(self):
        self.get_cli().cmd('ip link del dev '  + self.get_name())

    def up(self):
        self.get_cli().cmd('ip link set dev ' + self.get_name() + ' up')

    def down(self):
        self.get_cli().cmd('ip link set dev ' + self.get_name() + ' down')

    def add_ips(self, ip_list):
        self.ip_list = ip_list

    def get_ips(self):
        return self.ip_list
        
    def add_route(self, route_ip, gw_ip):
        self.get_cli().cmd('ip route add ' + route_ip[0] + '/' + route_ip[1] + ' via ' + gw_ip[0])

    def del_route(self, route_ip):
        self.get_cli().cmd('ip route del ' + route_ip[0] + '/' + route_ip[1])

    def get_near_host(self):
        return self.near_host

    def print_config(self, indent=0):
        print ('    ' * indent) + self.name + ' with ips: ' + str(self.ip_list)

