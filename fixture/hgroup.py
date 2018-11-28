import pexpect
import random
import subprocess
import shlex
from fixture.params import create_hgroup
from fixture.params import modify_hgroup
from fixture.params import del_hgroup
import pytest


class HGroupHelper:

    def __init__(self, app):
        self.app = app

    def create(self, hgroup, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('hgroup-add %s' % hgroup)
        adm.expect(create_hgroup['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(create_hgroup['02-desc'])
        adm.sendline()
        adm.expect('> ')
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def hgroup_info(self, hgroup, passfile):
        hgroupget = "ald-admin hgroup-get %s -f --pass-file=%s" % (hgroup, passfile)
        sproc = subprocess.Popen(shlex.split(hgroupget),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        assert not err
        return out.decode()

    def random_hgroup_get(self):
        hgroup_list = self.hgroup_list()
        return random.choice(hgroup_list)
        #return hgroup


    def hgroup_list(self):
        hgroup_list = "ald-admin hgroup-list"
        sproc = subprocess.Popen(shlex.split(hgroup_list),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        hgrouplist = out.decode()
        return list(hgrouplist.split('\n'))[0:-1]

    def hgroup_mod(self, hgroup, passfile):
        adm = self.app.ald_cmd(passfile)
        for key in sorted(modify_hgroup):
            adm.sendline('hgroup-mod {0} --{1}={2}'.format(hgroup, key, modify_hgroup[key]))
            adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def hgroup_mod_hosts(self, hgroup, host, opt, passfile):
        adm = self.app.ald_cmd(passfile)
        if opt == 'add':
            adm.sendline('hgroup-mod {0} --add-host --host={1}'.format(hgroup, host))
        if opt == 'rm':
            adm.sendline('hgroup-mod {0} --rm-host --host={1}'.format(hgroup, host))
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def hgroup_del(self, hgroup, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('hgroup-rm %s' % hgroup)
        adm.expect(del_hgroup['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(del_hgroup['02-confirm'])
        adm.sendline("yes")
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()


