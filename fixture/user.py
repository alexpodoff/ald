

import random
import pexpect
import subprocess
import shlex
import socket
from fixture.params import create_user
from fixture.params import create_user_parametrize
from fixture.params import modify_user
from fixture.params import del_user


class UserHelper:

    def __init__(self, app):
        self.app = app

    def user_create(self, user, a_passwd, u_passwd):
        """Create user with all default settings."""
        adm = self.app.ald_cmd()
        enter = adm.sendline
        adm.sendline('user-add %s' % user)
        # Put admin and new user passwords
        adm.expect(create_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(create_user['02-puser'] % user)
        adm.sendline(u_passwd)
        adm.expect(create_user['03-prepeat'])
        adm.sendline(u_passwd)
        # Use default values for all other params
        # (Like user just press Enter).
        for key in sorted(create_user.keys())[3:-1]:
            if '%s' in create_user[key]:
                adm.expect(create_user[key] % user)
            else:
                adm.expect(create_user[key])
            enter()
        adm.expect(create_user['18-correct'])
        adm.sendline('y')
        adm.expect('> ')
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_create_parametrize(self, user, xid, policy, a_passwd, u_passwd):
        """Create user with certain settings."""
        adm = self.app.ald_cmd()
        fqdn = socket.getfqdn()
        params = '--create-group --chg-pass --home-server={0}'.format(fqdn)
        # func creates params for user-add command like '--x=y' from dict in params.py
        combiner = lambda x, y: ' --' + x + '=' + y
        for key in sorted(create_user_parametrize):
            params = params + combiner(key, create_user_parametrize[key])
        adm.sendline('user-add {0} --uid={1} --gid={1} --policy={2} {3}'.format(user, xid, policy, params))
        adm.expect(create_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(create_user['02-puser'] % user)
        adm.sendline(u_passwd)
        adm.expect(create_user['03-prepeat'])
        adm.sendline(u_passwd)
        adm.expect(create_user['18-correct'])
        adm.sendline('y')
        adm.expect('> ')
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_info(self, user, passfile):
        userget = "ald-admin user-get %s -f --pass-file=%s" % (user, passfile)
        sproc = subprocess.Popen(shlex.split(userget),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        assert not err
        return out.decode()

    def user_full_info(self, user, passfile):
        userget = "ald-admin user-get --full %s -f --pass-file=%s" % (user, passfile)
        sproc = subprocess.Popen(shlex.split(userget),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        assert not err
        return out.decode()

    def random_user_get(self):
        user_list = self.user_list()
        user = random.choice(user_list)
        return user

    def user_list(self):
        user_list = "ald-admin user-list"
        sproc = subprocess.Popen(shlex.split(user_list),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        ulist = out.decode()
        return list(ulist.split())

    def user_mod(self, user, passfile, policy='default'):
        adm = self.app.ald_cmd(passfile)
        for key in sorted(modify_user):
            adm.sendline('user-mod {0} --{1}={2}'.format(user, key, modify_user[key]))
            adm.expect("> ")
        adm.sendline('user-mod %s --policy=%s' % (user, policy))
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_del(self, user, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('user-rm %s' % user)
        adm.expect(del_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(del_user['02-confirm'])
        adm.sendline("yes")
        adm.expect(del_user['03-gconfirm'])
        adm.sendline()
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_ald_cap(self, user, host, passfile):
        adm = self.app.ald_cmd(passfile)
        adm.sendline('user-ald-cap {0} --add-hosts --host={1}'.format(user, host))
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_maclev_mod(self, user, min_lev, max_lev, passfile):
        adm = self.app.ald_cmd(passfile)
        adm.sendline('user-mac {0} --min-lev-int={1} --max-lev-int={2}'.format(user, min_lev, max_lev))
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_maccat_mod(self, user, min_cat, max_cat, passfile):
        adm = self.app.ald_cmd(passfile)
        adm.sendline('user-mac {0} --min-cat-hex={1} --max-cat-hex={2}'.format(user, min_cat, max_cat))
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_aud_add(self, user, suc, fail, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('user-aud-add {0} --succ-hex={1} --fail-hex={2}'.format(user, suc, fail))
        adm.expect(create_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_aud_list(self, passfile):
        user_aud_list = 'ald-admin user-aud-list -f --pass-file=%s' % passfile
        sproc = subprocess.Popen(shlex.split(user_aud_list),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        audlist = out.decode()
        return list(audlist.split('\n'))

    def user_aud_mod(self, user, suc, fail, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('user-aud-mod {0} --succ-hex={1} --fail-hex={2}'.format(user, suc, fail))
        adm.expect(create_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_aud_del(self, user, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('user-aud-rm %s' % user)
        adm.expect(del_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(del_user['02-confirm'])
        adm.sendline("yes")
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_linux_cap_mod(self, user, cap, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('user-linux-cap {0} --{1}=1'.format(user, cap))
        adm.expect(create_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_parsec_cap_mod(self, user, cap, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('user-parsec-cap {0} --{1}=1'.format(user, cap))
        adm.expect(create_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_linux_cap_reset(self, user, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('user-linux-cap %s --reset' % user)
        adm.expect(create_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_parsec_cap_reset(self, user, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('user-parsec-cap %s --reset' % user)
        adm.expect(create_user['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def user_aud_check(self, log, call='open', obj=None, flag='[s]', user=None):
        """
        The comparison fields of a log line in log list with keyword arguments.

        Split line, then compare line parts with must-be-values.
        If all fields are equal in line - break the cycle and return True,
        else - False.
        :param log: list
        :param obj: str
        :param call: str
        :param user: str
        :param flag: str
        :return: boolean
        """
        result = False
        for line in log:
            aud_line = line.split()
            if user:
                if obj:
                    if obj not in aud_line[9]:
                        result = False
                    elif call not in aud_line[9]:
                        result = False
                    elif flag != aud_line[8]:
                        result = False
                    elif user != int(aud_line[7].split(',')[2]):
                        result = False
                    else:
                        result = True
                        break
                else:
                    if call not in aud_line[9]:
                        result = False
                    elif flag != aud_line[8]:
                        result = False
                    elif user != int(aud_line[7].split(',')[2]):
                        result = False
                    else:
                        result = True
                        break
            else:
                if obj:
                    with open('/tmp/1', 'w') as a:
                        a.write(str(flag))
                    if obj not in aud_line[9]:
                        result = False
                    elif call not in aud_line[9]:
                        result = False
                    elif flag != aud_line[8]:
                        result = False
                    else:
                        result = True
                        break
                else:
                    if call not in aud_line[9]:
                        result = False
                    elif flag != aud_line[8]:
                        result = False
                    else:
                        result = True
                        break
        return result
