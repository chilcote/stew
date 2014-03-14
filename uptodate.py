#!/usr/bin/python2.7

import os
import sys
import re
import subprocess
import hashlib

CONFIG = os.path.join(os.getenv('HOME'), '.stew_config')

def run_cmd(cmd, stream_out=False):
    """Runs a command and returns a tuple of stdout, stderr, returncode."""
    if stream_out:
        task = subprocess.Popen(cmd)
    else:
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    (stdout, stderr) = task.communicate()
    return stdout, stderr, task.returncode

def get_config_data(config, category):
    """Returns data from config file."""
    f = open(config, 'r')
    for line in f.readlines():
        if category in line:
            line = line.rstrip()
            return line.split('=')[1]
    f.close

def get_checksum(pkg):
    """Returns sha1 checksum of package."""
    statinfo = os.stat(pkg)
    if statinfo.st_size/1048576 < 200:
        f_content = open(pkg, 'r').read()
        f_hash = hashlib.sha1(f_content).hexdigest()
        return f_hash
    else:
        cmd = ['shasum', pkg]
        (stdout, unused_sterr, unused_rc) = run_cmd(cmd)
        return stdout.split()[0]

def get_webserver(config_file):
    f = open(config_file, 'r')
    for line in f.readlines():
        if "webserver" in line:
            line = line.rstrip()
            return line.split('=')[1]

def upload_pkg(pkg, login, webserver, serverpath):
    """Uploads package."""
    cmd = ['scp', pkg, '%s@%s:%s' % (login, webserver, serverpath)]
    run_cmd(cmd)

def main():
    if not os.path.exists(CONFIG):
        print 'Your stew environment has not been configured.' \
                '\nPlease run stew -c to create a config file.'
        sys.exit(1)
    if len(sys.argv) != 2:
        print 'Usage: uptodate.py /path/to/package'
        sys.exit(1)
    webserver = get_config_data(CONFIG, 'webserver')
    serverpath = get_config_data(CONFIG, 'path')
    webpath = os.path.basename(serverpath)
    login = get_config_data(CONFIG, 'login')
    package = sys.argv[1]
    upload_pkg(package, login, webserver, serverpath)
    print os.path.basename(package), get_checksum(package)

if __name__ == '__main__':
  main()
