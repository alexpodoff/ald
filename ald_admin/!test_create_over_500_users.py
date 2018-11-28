"""Test module for adding over 500 users."""


import random
from .ald_admin_data import valid_name_generator, password_generator

__author__ = 'pod'
__version__ = '0.1'


def test_create_validname_user(ald_init, app):
    """Create user with all default settings."""
    user_password = password_generator()
    admpass = ald_init[0]
    passfile = ald_init[1]
    count = len(app.user.user_list())
    user_count = 500 + random.choice(range(1, 20))
    while count != user_count:
        user = valid_name_generator()
        app.user.user_create(user, admpass, user_password)
        user_info = app.user.user_info(user, passfile)
        count += 1
        assert user in user_info
    assert len(app.user.user_list()) == count
