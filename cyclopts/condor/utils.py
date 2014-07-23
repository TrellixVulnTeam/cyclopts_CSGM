from __future__ import print_function

import warnings
import tables as t
import shutil
import time
import os
import io
import glob 
import uuid
import re

try:
    import paramiko as pm
    import tarfile
    from datetime import datetime
    import getpass
    import glob
except ImportError:
    warnings.warn(("The Condor module was not able to "
                   "import its necessary modules"), ImportWarning)

from cyclopts import tools

batlab_base_dir_template = u"""/home/{user}"""

tar_output_cmd = """
cd {remotedir} && tar -czf {tardir}.tar.gz {re}
"""

def _wait_for_cmd(stdout, t_sleep=5):
    """Returns after a cmd's stdout reports that it has finished"""
    while not stdout.channel.exit_status_ready():
        print('Command not complete, checking again in {0} seconds.'.format(
                t_sleep))
        time.sleep(t_sleep)
        
def _wait_till_found(client, path, t_sleep=5):
    """Queries a client if a an expected file exists until it does."""
    print('Waiting for existence of {0}'.format(path))
    found = False
    while not found:
        cmd = "find {0}".format(path)
        print("Remotely executing '{0}'".format(cmd))
        stdin, stdout, stderr = client.exec_command(cmd)
        found = len(stdout.readlines()) > 0
        if not found:
            print('Not there yet! Checking again in {0} seconds.'.format(
                    t_sleep))
            time.sleep(t_sleep)

def _wait_till_done(client, user, host, keyfile, pid, t_sleep=300):
    """Queries a client if a an expected process is done."""
    done = False
    while not done:
        print("Querying status of {0}".format(pid))
        print("connecting to {0}@{1}".format(user, host))
        client.connect(host, username=user, key_filename=keyfile)
        done = _check_finish(client, pid)
        client.close()
        if not done:
            print('Not done yet! Checking again in {0} minutes.'.format(
                    t_sleep / 60.))
            time.sleep(t_sleep)

def _check_finish(client, pid):
    """Checks the status of a condor run on the client.
    """
    cmd = "condor_q {0}".format(pid)
    print("Remotely executing '{0}'".format(cmd))
    stdin, stdout, stderr = client.exec_command(cmd)
    outlines = stdout.readlines()
    done = False
    donecheck = 'ID'
    if len(outlines) > 0 and len(outlines[-1].split()) > 0 \
            and outlines[-1].split()[0].strip() == donecheck:
        done = True
    return done

def rm(user, host="submit-3.chtc.wisc.edu", keyfile=None, expr=None):
    client = pm.SSHClient()
    client.set_missing_host_key_policy(pm.AutoAddPolicy())
    _, keyfile, pw = tools.ssh_test_connect(client, host, user, keyfile=keyfile, 
                                            auth=False)
    client.connect(host, username=user, key_filename=keyfile, password=pw)
    print("connecting to {0}@{1}".format(user, host))
    
    cmd = "condor_q {user}".format(user=user)
    print("Remotely executing '{0}'".format(cmd))
    stdin, stdout, stderr = client.exec_command(cmd)
    
    expr = user if expr is None else expr
    cexpr = re.compile(expr)
    pids = [l.split()[0] for l in stdout.readlines() if cexpr.search(l)]
    
    if len(pids) > 0:
        cmd = "condor_rm {pids}".format(pids=" ".join(pids))
        print("Remotely executing '{0}'".format(cmd))
        stdin, stdout, stderr = client.exec_command(cmd)
    else:
        print("No jobs found matching {0}.".format(expr))
    client.close()
        
def collect(localdir, remotedir, user, host="submit-3.chtc.wisc.edu", 
            outdb='cyclopts_results.h5', clean=False, keyfile=None):
    client = pm.SSHClient()
    client.set_missing_host_key_policy(pm.AutoAddPolicy())
    _, keyfile, pw = tools.ssh_test_connect(client, host, user, keyfile, auth=True)

    client.connect(host, username=user, key_filename=keyfile, password=pw)
    print("connecting to {0}@{1}".format(user, host))

    if not os.path.exists(localdir):
        os.makedirs(localdir)    

    # get files and clean up
    nfiles = get_files(client, remotedir, localdir, '*_out.h5')
    
    if clean:
        cmd = "rm -r {0} && rm {0}.tar.gz".format(remotedir)
        print("Remotely executing '{0}'".format(cmd))
        stdin, stdout, stderr = client.exec_command(cmd)
    client.close()
    
    # combine files and clean up
    files = glob.iglob(os.path.join(localdir, '*_out.h5'))
    stmt = "Combining {0} databases into {1}".format(nfiles, outdb)
    print(stmt)
    tools.combine(files, new_file=outdb, clean=True)

def get_files(client, remotedir, localdir, re):
    """Retrieves all files matching an expression on a remote site.

    Parameters
    ----------
    client : paramiko SSHClient
        the client
    remotedir : str
        the output directory on the client machine
    localdir : str
        the output directory on the local macine
    re : str
        the pattern to match
    """
    tardir = 'outfiles'
    cmd = tar_output_cmd.format(remotedir=remotedir, tardir=tardir, re=re)
    print("Remotely executing '{0}'".format(cmd))
    stdin, stdout, stderr = client.exec_command(cmd)
    _wait_for_cmd(stdout)
    
    remotetar = os.path.join(remotedir, '{0}.tar.gz'.format(tardir))
    localtar = os.path.join(localdir, '{0}.tar.gz'.format(tardir))
    ftp = client.open_sftp()
    print("Copying {0} from condor submit node to {1}.".format(
            remotetar, localtar))
    ftp.get(remotetar, localtar)
    ftp.close()

    with tarfile.open(localtar, 'r:gz') as f:
        files = f.getnames()
        nfiles = len(files)
        f.extractall(localdir)
    
    print("retrived {0} files from tarball".format(nfiles))

    os.remove(localtar)
    return nfiles
