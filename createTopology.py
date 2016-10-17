#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Nicolás Boettcher
#
# Mininet Tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mininet Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

import networkx as nx
import matplotlib.pyplot as plt

def remove_char(text):
    output=''
    for i in text:
        # text without commas and spaces
        if not (i==' ' or i==','):
            output+=i
    return output

filename_r="AttMpls.graphml"
# TODO check all with geolocation
#filename_r="Chinanet.graphml"
g=nx.read_graphml(filename_r)

# uses canonical switch name
host_switches=False

filename_w="topology.py"

for node in g.nodes(data=True):
    print(node)

for edge in g.edges(data=True):
    a=edge
    print(a)

# Start to create filename_w
archivo = open(filename_w, 'w')
archivo.write('from mininet.topo import Topo\n')
archivo.write('class MinimalTopo(Topo):\n')
archivo.write('\tdef build(self):\n')
archivo.write('\t\t#Create devices\n')

# Create devices
# TODO change \t by only 4 spaces
# Initial DataPath ID
dpid=1000
for i in g.node.keys():
    tmp = ''
    if not ('host' in g.node[i] or 'switch' in g.node[i]):
        if 'label' in g.node[i]:
            tmp += remove_char(g.node[i]['label'])[:10]
        if 'cpu' in g.node[i]:
            tmp+=',cpu='+g.node[i]['cpu']

        if host_switches:
            #TODO if uses canonical switch name automatically enters here
            if g.node[i]['label'][0]=='h':
                archivo.write("\t\t%s = self.addHost('%s')\n" % (remove_char(g.node[i]['label'])[:10], tmp))
            elif g.node[i]['label'][0]=='s':
                archivo.write("\t\t%s = self.addSwitch('%s')\n" % (remove_char(g.node[i]['label'])[:10], tmp))
        else:
            archivo.write("\t\t%s = self.addSwitch('%s',dpid='000000000000%d')\n" % (remove_char(g.node[i]['label'])[:10], tmp, dpid))
            dpid+=1

        #Change coordinates
        #TODO check all nodes with geolocation
        #Gephi standar
        if 'x' in g.node[i] and 'y' in g.node[i]:
            g.node[i]['pos']=(g.node[i]['x'],g.node[i]['y'])
        #Topology Zoo standar
        elif 'Latitude' in g.node[i] and 'Longitude' in g.node[i]:
            g.node[i]['pos']=(g.node[i]['Longitude'],g.node[i]['Latitude'])

#Create links
archivo.write('\t\t#Create links\n')
for edge in g.edges(data=True):
    tmp=''
    tmp += "'" + remove_char(g.node[edge[0]]['label'])[:10] + "','" + remove_char(g.node[edge[1]]['label'])[:10] + "'"
    if 'bw' in edge[2]:
        tmp+=', bw='+edge[2]['bw']
    elif 'LinkSpeed' in edge[2]:
        tmp+=', bw='+edge[2]['LinkSpeed']
    if 'delay' in edge[2]:
        tmp += ', delay=' + edge[2]['delay']
    if 'loss' in edge[2]:
        tmp += ', loss=' + edge[2]['loss']
    if 'max_queue_size' in edge[2]:
        tmp += ', max_queue_size=' + edge[2]['max_queue_size']
    if 'use_htb' in edge[2]:
        tmp += ', use_htb=' + edge[2]['use_htb']

    archivo.write("\t\tself.addLink(%s)\n" % (tmp))

archivo.write('topos = {\n')
archivo.write("\t'minimal': MinimalTopo\n")
archivo.write('}')

archivo.close()
nx.draw(g, nx.get_node_attributes(g, 'pos'), with_labels=True)
plt.show()