"""Test for inability of adding invalid names of mac-levels"""

import random
import string
from .ald_admin_data import invalid_mac_generator

__author__ = 'pod'
__version__ = '0.1'


def test_create_invalidname_maclev(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    maclev_list = app.macattr.maclev_list()
    if len(maclev_list) == 255:
        maclev = app.macattr.random_maccat_get()
        while list(maclev.keys())[0] == 0:
            app.macattr.maclev_del(app.macattr.random_maccat_get(), admpass)
    maclev_bad_list = invalid_mac_generator()
    digit = random.choice(list(maclev_list.keys()))
    maclev_bad_list.append(digit)
    numb = random.choice(string.digits)
    while int(numb) in list(maclev_list.keys()):
        numb = random.choice(string.digits)
    for name in maclev_bad_list:
        app.macattr.maclev_invalid_create(numb, name, passfile)
        maclev_list_new = app.macattr.maclev_list()
        assert maclev_list_new == maclev_list
