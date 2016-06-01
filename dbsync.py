'''
    Copyright (C) 2016 Lion Cui <lioncui@163.com>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

#!/usr/bin/python
#-*- coding:utf8 -*-
import pymysql
import time
import json
import urllib2
import config
key = 'q5mTrTGzCSVq5QmGpI9y18Bo'
ipurl = 'http://api.map.baidu.com/location/ip?ak='+key+'&coor=bd09ll&ip='
sqlarr = []

host = config.DBHOST
port = int(config.DBPORT)
user = config.DBUSER
password = config.DBPASS
db = config.DBNAME

def getGeo(ip):
    try:
        u = urllib2.urlopen(ipurl+ip)
        page = json.load(u)
        #if 'content' in page:
            #point = page['content'].get('point')
            #print 'ip %s has geoX %s and geoY %s' % (ip,point['x'],point['y'])
        if 'address' in page:
            address = page.get('address').split("|")[1].encode("utf-8")
            return address
    except Exception as e:
        return None

def format_log(f):
    #f = open(log)
    res = {}
    know_ip_address = {}

    for l in f:
        arr = l.split(' ')
        ip = arr[0]
        if ip not in know_ip_address:
            address = getGeo(ip)
            know_ip_address[ip] = address
        #timestr = arr[3] + arr[4]
        #timestamp = time.strptime(timestr, "[%d/%b/%Y:%H:%M:%S+0800]")
        #timestamp = time.strftime("%Y-%m-%d %H:%M",timestamp)
        url = arr[6]
        status = arr[8]
        res[(ip,know_ip_address[ip],url,status)] = res.get((ip,know_ip_address[ip],url,status),0)+1
    f.close()
    res_list = [(k[0],k[1],k[2],k[3],v) for k,v in res.items()]
    return res_list

def exportmysql(f):
    conn = pymysql.connect(host = host,
                            port = port,
                            user = user,
                            password = password,
                            db = db,
                            charset = 'utf8',
                            cursorclass = pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cur:
            for s in format_log(f):
                sql = "INSERT INTO `log` (`ip`, `address`, `url`, `status`, `num`) VALUES ('%s', '%s', '%s', '%s', '%s')" % s
                cur.execute(sql)
            conn.commit()
        return "Sync"
    except Exception as e:
        return e
    finally:
        conn.close()