import random
import pexpect
import pytest
import subprocess
import shlex
from fixture.params import create_host
from fixture.params import modify_host
from fixture.params import del_host


class HostHelper:

    def __init__(self, app):
        self.app = app

    def create(self, host, a_passwd):
        """Create host with all default settings."""
        adm = self.app.ald_cmd()
        enter = adm.sendline
        adm.sendline('host-add %s' % host)
        adm.expect(create_host['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(create_host['02-desc'])
        adm.sendline()
        adm.expect(create_host['03-confirm'])
        adm.sendline('y')
        adm.expect('> ')
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def host_info(self, host, passfile):
        hostget = "ald-admin host-get %s --full -f --pass-file=%s" % (host, passfile)
        sproc = subprocess.Popen(shlex.split(hostget),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        assert not err
        return out.decode()

    def random_host_get(self):
        host_list = self.host_list()
        host = random.choice(host_list)
        return host

    def host_list(self):
        host_list = "ald-admin host-list"
        sproc = subprocess.Popen(shlex.split(host_list),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        hostlist = out.decode()
        return list(hostlist.split())

    def host_mod(self, host, passfile):
        adm = self.app.ald_cmd(passfile)
        for key in sorted(modify_host):
            adm.sendline('host-mod {0} --{1}={2}'.format(host, key, modify_host[key]))
            adm.expect("> ")
#        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def host_del(self, host, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('host-rm %s' % host)
        adm.expect(del_host['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(del_host['02-confirm'])
        adm.sendline("yes")
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()


if __name__ == '__main__':
    print(sys.path)
