#!/usr/bin/python
#-*- coding=utf-8 -*-
"""dig trace"""

import random
import re
import subprocess
import sys


class MyDig():
    """dig 类"""
    def __init__(self, domain):
        self.root_dns = []
        self.domain = domain
        tmp = "abcdefghijklm"
        for one_char in tmp:
            self.root_dns.append('%s.root-servers.net.' % one_char)

    def single_dig(self, servers):
        """dig 单个域名返回结果"""
        server = random.choice(servers)
        print "choose %s randomly" % server
        fp = subprocess.Popen('dig %s @%s' % (self.domain, server), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_out = fp.stdout.read()
        ret_dict = self.deal_out(print_out)
        if len(ret_dict['ANSWER SECTION']) > 0:
            print ';; ANSWER SECTION'
            for line in ret_dict['ANSWER SECTION']:
                print line

        print ';; AUTHORITY SECTION'
        for line in ret_dict['AUTHORITY SECTION']:
            print line
        print ""
        return ret_dict

    def deal_out(self, print_out):
        """处理单个dig的输出，返回结果"""
        ret_dict = {'ANSWER SECTION': [], 'AUTHORITY SECTION': [], 'ADDITIONAL SECTION': []}
        lines = print_out.split('\n')
        flag = ''
        for line in lines:
            line = line.strip()
            if line == '':
                flag = ''
                continue

            if flag != '':
                ret_dict[flag].append(line)

            for key in ret_dict:
                if key in line:
                    flag = key
        return ret_dict

    def global_head(self):
        """输出根授权DNS地址"""
        print ";; global options: +cmd"
        for server in self.root_dns:
            print ".                                             518400    IN            NS            %s" % server
        print ""

    def dig(self):
        """递归查询"""
        return_flag = False
        match_pattern = r'IN\W*\b(CNAME|A)\b'
        server_list = self.root_dns
        self.global_head()
        while not return_flag:
            ret_dict = self.single_dig(server_list)
            new_server_list = []

            for line in ret_dict['ANSWER SECTION']:
                if re.search(match_pattern, line):
                    return_flag = True

            if not return_flag:
                for line in ret_dict['AUTHORITY SECTION']:
                    new_server_list.append(line.split()[-1])
                server_list = new_server_list

if __name__ == "__main__":
    DOMAIN = sys.argv[1]
    DIG = MyDig(DOMAIN)
    DIG.dig()
