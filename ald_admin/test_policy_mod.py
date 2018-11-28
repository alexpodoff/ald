

from fixture.params import modify_policy as mp

__author__ = 'pod'
__version__ = '0.2'


def test_policy_mod(ald_init, app):
    """Modify policy with test settings."""
    admpass = ald_init[0]
    passfile = ald_init[1]
    policy_list = app.policy.policy_list(passfile)
    if policy_list == ['default']:
        app.policy.create_policy('testpolicy', admpass)
    policy = app.policy.random_policy_get(passfile)
    app.policy.policy_mod(policy, passfile)
    policy_info = app.policy.policy_info(policy, passfile)
    assert policy in policy_info
    assert 'Максимальное время жизни пароля: %s' % mp['max-life'] in policy_info
    assert 'Минимальное время жизни пароля: %s' % mp['min-life'] in policy_info
    assert 'Минимальная длина пароля: %s' % mp['min-length'] in policy_info
    assert 'Минимальное число классов символов в пароле: %s' % mp['min-classes'] in policy_info

