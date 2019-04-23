#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader
from config.settings import settings

curDir = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))


class Report(object):
    def __init__(self, docName=None, docDir=curDir, xmlName='report.xml'):
        self.docName = docName
        self.date = {'stime': settings.StartTime, 'etime': settings.EndTime}
        self.hosts = []
        self.tables = []
        self.graphs = []
        self.xml = self.loader(docDir, xmlName)

    def loader(self, docDir, xmlName):
        loader = FileSystemLoader(searchpath=docDir, encoding='utf-8')
        return Environment(loader=loader).get_template(xmlName)

    def add_host(self, name, ip):
        host = {'name': name, 'host': ip}
        self.hosts.append(host)
        return self.hosts

    def add_table(self, table):
        '''
            table = {
                'host': 'host',
                'metrics': [{
                    'name': 'name',
                    'minimum': '',
                    'average': '',
                    'maximum': '',
                    'peak_times': ''
                }]
            }
        '''

        self.tables.append(table)
        return self.tables

    def add_graph(self, graph):
        '''
            graph = {
                'host': 'host',
                'graphs': []
            }
        '''
        self.graphs.append(graph)
        return self.graphs

    def save(self):
        xml = self.xml.render({
            'date': self.date,
            'hosts': self.hosts,
            'tables': self.tables,
            'graphs': self.graphs}).encode('utf-8')
        self.docName = self.docName if self.docName.endswith('.doc') else self.docName + '.doc'
        docOutDir = os.path.join(settings.BASE_DIR, r'output/docs')
        with open(os.path.join(docOutDir, self.docName), 'wb') as f:
            f.write(xml)
        return xml


if __name__ == '__main__':
    f = Report('tests')
    f.save()

