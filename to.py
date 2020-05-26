#!/usr/bin/env python3
# coding=utf-8

__author__ = 'wangys2'
import os, re, sys

os.chdir('/home/www/brande/')
url = "http://127.0.0.1/ansible/"
name = "hosts"
get_cmd = "wget -q -T 2 -t 1 %s%s  -O %s" % (url, name, name)

exit_status = os.system(get_cmd)

if exit_status != 0:
    print("can not download the hosts file")
    sys.exit()

hosts_files = name

def get_hosts_info(hosts_files):
    hosts_info = {}
    with open(hosts_files) as hosts:
        for i in hosts:
            if i.startswith('[shutdown'):
                break
            if i.startswith('[') and not i.startswith('[shutdown'):
                comment = i.strip('\n').strip('[').strip(']')
                continue
            if i.startswith('1'):
                host_ip = i.split(' ')[0].strip('\n')
                hosts_info.setdefault(host_ip, []).append(comment)
    return hosts_info


def ssh_login(host):
    global flag
    list = []
    key = '/home/www/gihtg_key/id_rsa'
    for x, y in hosts_info.items():
        if host == x:
            os.system('ssh -i %s %s' % (key, host))
            flag = False
        if host in y:
            list.append(x)
    if len(list) > 1:
        print(list)
    if len(list) == 1:
        os.system('ssh -i %s %s' % (key, list[0]))
        flag = False
        #print "just one host "#%s" % list[0]


hosts_info = get_hosts_info(hosts_files)


flag = True

try:
    host = sys.argv[1]
    ssh_login(host)
except:
    pass

while flag:
    #print flag
    host = input('please input host name:')
    if host == 'list':
        for x, y in hosts_info.items():
            print('%s:%s' %(x, y))
    elif host == 'exit':
        sys.exit()
    else:
        ssh_login(host)

