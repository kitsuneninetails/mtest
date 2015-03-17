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

from MTestInterface import Interface


class VirtualInterface(Interface):
    def __init__(self, name, near_host, far_iface_name, far_host, peer_ext='.p'):
        super(VirtualInterface, self).__init__(name, near_host)
        self.peer_name = self.get_name() + peer_ext
        self.far_host = far_host
        self.far_iface_name = far_iface_name

    def setup(self):
        # add a veth-type interface with a peer
        self.get_cli().cmd('ip link add dev ' + self.get_name() + ' type veth peer name ' + self.peer_name)
        # move peer iface onto far host's namespace
        self.get_cli().cmd('ip link set dev ' + self.peer_name + ' netns ' +
                           self.far_host.get_name() + ' name ' + self.far_iface_name)
        # add ips
        for ip in self.ip_list:
            self.far_host.get_cli().cmd('ip addr add ' + ip[0] + '/' + ip[1] + ' dev ' + self.far_iface_name)

    def up(self):
        # Set main iface up
        super(VirtualInterface, self).up()
        # Set peer iface up on far host's namespace
        self.far_host.get_cli().cmd('ip link set dev ' + self.far_iface_name + ' up')
        
    def down(self):
        super(VirtualInterface, self).down()
        self.far_host.get_cli().cmd('ip link set dev ' + self.far_iface_name + ' down')

    def add_peer_route(self, route_ip, gw_ip):
        self.far_host.get_cli().cmd('ip route add ' + route_ip[0] + '/' + route_ip[1] + ' via ' + gw_ip[0])

    def del_peer_route(self, route_ip):
        self.far_host.get_cli().cmd('ip route del ' + route_ip[0] + '/' + route_ip[1])

    def get_far_host(self):
        return self.far_host

    def get_far_host_interface_name(self):
        return self.far_iface_name

    def print_config(self, indent=0):
        print ('    ' * indent) + self.name + ' linked as ' + self.far_host.get_name() + '/' \
            + self.far_iface_name + ' with ips: ' + str(self.ip_list)