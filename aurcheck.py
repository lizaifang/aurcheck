#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
#import AUR.RPC as AUR
from AUR.RPC import AUR
from time import localtime, strftime 
from pycman import config
import pyalpm

if __name__ == '__main__':
    h = config.init_with_config("/etc/pacman.conf")
    #print(h.get_localdb().pkgcache)
    installed = set(h.get_localdb().pkgcache)
    #print(h.get_localdb().get_pkg('mysql'))
    #print(h.get_localdb().grpcache)
    #print(installed)
    aur = AUR()
    #print(aur.info('mysql'))
    #[{'ID': 69409, 'NumVotes': 4, 'OutOfDate': 0, 'CategoryID': 2, 'FirstSubmitted': 1366917203, 'Version': '5.6.13-1', 'URL': 'https://www.mysql.com/products/community/', 'LastModified': 1375714132, 'Name': 'mysql', 'Maintainer': 'rustam', 'Description': 'A fast SQL database server', 'License': 'GPL', 'URLPath': '/packages/my/mysql/mysql.tar.gz'}]
    #print(aur.info(('mysql','heidisql')))
    #[{'NumVotes': 4, 'Version': '5.6.13-1', 'URL': 'https://www.mysql.com/products/community/', 'Name': 'mysql', 'License': 'GPL', 'FirstSubmitted': 1366917203, 'Maintainer': 'rustam', 'URLPath': '/packages/my/mysql/mysql.tar.gz', 'ID': 69409, 'OutOfDate': 0, 'LastModified': 1375714132, 'Description': 'A fast SQL database server', 'CategoryID': 2}, {'NumVotes': 9, 'ID': 65392, 'URL': 'http://www.heidisql.com/', 'Name': 'heidisql', 'License': 'GPL', 'FirstSubmitted': 1355313819, 'Maintainer': 'crush', 'URLPath': '/packages/he/heidisql/heidisql.tar.gz', 'Version': '7.0-2', 'OutOfDate': 1372029392, 'LastModified': 1355314287, 'Description': 'A lightweight, Windows based interface for managing MySQL and Microsoft SQL databases. (uses Wine).', 'CategoryID': 3}]
    #display_fields = ('LocalVersion','Version', 'LastModified')
    #aurpkg['LastModified'] = strftime('%Y-%m-%d %H:%M:%S', localtime(aurpkg['LastModified']))
    offical_repo = ['core', 'extra', 'community', 'multilib']
    for db in h.get_syncdbs():
        if db.name in offical_repo:
            for item in list(installed):
                if db.get_pkg(item.name):
                    installed.remove(item)
            #print(pkg)
            #pkgname = pkg.name
            #syncpkg = db.get_pkg(pkgname)
            #print(syncpkg)
    #print(installed)
    pkgs = [pkg.name for pkg in installed]
    for item in aur.info(pkgs):
        for localpkg in installed:
            if localpkg.name == item['Name']:
                if pyalpm.vercmp(item['Version'], localpkg.version) != 0:
                    if pyalpm.vercmp(item['Version'], localpkg.version) > 0:
                        eq = '\033[1;31m=>\033[0m'
                        #eq = '\033[1;37;40m=>\033[2;32;40m'
                    else:
                        eq = '<='
                    print(localpkg.name, localpkg.version, eq, item['Version'])
