
import subprocess
import pexpect
import random
import shlex
from fixture.params import create_maclev
from fixture.params import del_maclev


class MacAttrHelper:

    def __init__(self, app):
        self.app = app

    def maclev_list(self):
        maclev_list = "ald-admin maclev-list"
        sproc = subprocess.Popen(shlex.split(maclev_list),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        maclevlist = out.decode()
        maclevlist = list(maclevlist.split('\n'))[:-1]
        keys = []
        vals = []
        for i in maclevlist:
            keys.append(int(i.split(':')[0]))
            vals.append(i.split(':')[1][1:])
        return dict(zip(keys, vals))

    def random_maclev_get(self):
        maclev = random.choice(list(self.maclev_list().items()))
        return {maclev[0]: maclev[1]}

    def maclev_create(self, numb, maclev, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('maclev-add %s %s' % (numb, maclev))
        adm.expect(create_maclev['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect('> ')
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def maclev_invalid_create(self, numb, maclev, passfile):
        adm = self.app.ald_cmd(passfile)
        adm.sendline('maclev-add %s %s' % (numb, maclev))
        adm.expect('> ')
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def maclev_mod(self, maclev, new_name, passfile):
        adm = self.app.ald_cmd(passfile)
        adm.sendline('maclev-mod {0} {1}'.format(maclev, new_name))
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def maclev_del(self, maclev, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('maclev-rm %s' % maclev)
        adm.expect(del_maclev['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(del_maclev['02-confirm'])
        adm.sendline("yes")
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def maccat_list(self):
        maccat_list = "ald-admin maccat-list"
        sproc = subprocess.Popen(shlex.split(maccat_list),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        maccatlist = out.decode()
        maccatlist = list(maccatlist.split('\n'))[:-1]
        keys = []
        vals = []
        for i in maccatlist:
            keys.append(i.split(':')[0])
            vals.append(i.split(':')[1][1:])
        return dict(zip(keys, vals))

    def random_maccat_get(self):
        maccat = random.choice(list(self.maccat_list().items()))
        return {maccat[0]: maccat[1]}

    def maccat_create(self, cat, name, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('maccat-add %s %s' % (cat, name))
        adm.expect(create_maclev['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect('> ')
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def maccat_mod(self, maccat, new_name, passfile):
        adm = self.app.ald_cmd(passfile)
        adm.sendline('maccat-mod {0} {1}'.format(maccat, new_name))
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def maccat_del(self, maccat, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('maccat-rm %s' % maccat)
        adm.expect(del_maclev['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(del_maclev['02-confirm'])
        adm.sendline("yes")
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()
