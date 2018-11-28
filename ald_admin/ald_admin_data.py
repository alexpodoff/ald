"""Test data for ald-admin utility tests."""

import string
import random
import re

__author__ = 'pod'
__version__ = '0.2'


def password_generator(length=8):
    """Create random password
     :return: str
     """
    char_classes = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation
    ]
    password = ''
    while len(password) < length:
        if len(char_classes) > 0:
            char_class = random.choice(char_classes)
            char_classes.remove(char_class)
        else:
            char_class = string.ascii_letters + string.digits
        char_class_count = random.randint(2, 3)

        while char_class_count > 0:
            password = password + random.choice(char_class)
            char_class_count -= 1

    return password[:length]


def valid_usernames_generator():
    """Generate the list of valid usernames.
     :return: list
     """
    # Generate one-character name and a name with all digits '_' and ' '.
    max_length = 31
    names = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_lowercase) + string.digits + '_' + '-',
    ]
    valid_chars = string.ascii_lowercase + string.digits + '_' + '-'
    # Create a name with max length.
    long = random.choice(string.ascii_lowercase)
    while len(long) <= max_length - 1:
        long = long + random.choice(valid_chars)
    names.append(long)
    # Create some valid random names.
    while len(names) < 6:
        length = random.randint(1, max_length - 1)
        # First character must be ASCII lowercase.
        name = random.choice(string.ascii_lowercase)
        while len(name) <= length:
            name = name + random.choice(valid_chars)
        names.append(name)
    return names


def valid_hgroupname_generator():
    """Generate the list of valid hgroupnames
     :return: list
     """
    # Generate one-character name and a name with all digits '_' and ' '.
    max_length = 31
    names = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_lowercase) + string.digits + '_' + '-',
    ]
    valid_chars = string.ascii_lowercase + string.digits + '_' + '-'
    # Create a name with max length.
    long = random.choice(string.ascii_lowercase)
    while len(long) <= max_length - 1:
        long = long + random.choice(valid_chars)
    names.append(long)
    # Create some valid random names.
    while len(names) < 6:
        length = random.randint(1, max_length - 1)
        # First character must be ASCII lowercase.
        name = random.choice(string.ascii_lowercase)
        while len(name) <= length:
            name = name + random.choice(valid_chars)
        names.append(name)
    return names


def valid_maclev_generator():
    """
    Generates a random valid name (max 31 char) for mac-level that contains ascii lower/uppercase,
    digits, special symbols '_', '-' and '.'
     Name can't start with '-'
    :return: str
    """
    max_length = 31
    rus_chars = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
    valid_chars = string.ascii_lowercase + string.ascii_uppercase + \
                  string.digits + rus_chars + str.upper(rus_chars) + '_' + '-' + '.'
    # first letter must not be '-' or digit
    first_letter = re.sub('-', '', valid_chars)
    first_letter = re.sub(string.digits, '', first_letter)
    name = random.choice(first_letter)
    length = random.randint(1, max_length - 1)
    while len(name) <= length:
        name = name + random.choice(valid_chars)
    return name


def invalid_mac_generator():
    """
    Generates a list of invalid names of mac-levels and categories
    including one long name (32 chars), one starts with '-'
    and names consists invalid chars ('!@#$%^&*()=+><?\|/~,;:`")
    :return: list
    """
    bad_chars = '!@#$%^&*)(=+><?\|/~,;:`"' + "'"
    names = [
        '-' + random.choice(string.ascii_letters),
    ]
    # can't check while it's bug on the name length
    # long_name = random.choice(string.ascii_letters)
    # while len(long_name) != 32:
    #    long_name = long_name + random.choice(string.ascii_letters)
    # names.append(long_name)
    for char in bad_chars:
        name = random.choice(string.ascii_letters) + char
        names.append(name)
    return names


def mac_level_combinations_generator():
    """
    Generates a list of 5 pairs of mac-levels
    min:0 max:random int
    min:0 max:255
    min:255 max:255
    random min/max and random min=max
    :return: list
    """
    levels = [
        [0, random.choice(range(1, 254))],
        [0, 255],
        [255, 255]
    ]
    rand = sorted([random.choice(range(1, 224)) for level in range(1, 3)])
    while rand[0] == rand[1]:
        rand = sorted([random.choice(range(1, 224)) for level in range(1, 3)])
    levels.append(rand)
    levels.append([rand[0], rand[0]])
    return levels


def mac_level_invalid_generator():
    """
    Generates a list of 2 pairs of mac-levels
    min:random max:0
    min:random max<min
    :return: list
    """
    levels = [
        [random.choice(range(1, 254)), 0]
    ]
    rand = [random.choice(range(1, 224)), random.choice(range(1, 224))]
    while rand[0] <= rand[1]:
        rand = [random.choice(range(1, 224)), random.choice(range(1, 224))]
    levels.append(rand)
    return levels

def mac_cat_hex_value_list():
    """
    Generates a list of decimal values of possible mac-cats
    :return: list
    """
    maccat_need = 64
    maccat_int = []
    while maccat_need != 0:
        a = sum(maccat_int)
        maccat_int.append(a + 1)
        maccat_need -= 1
    maccat_hex_value = [i for i in maccat_int]
    return maccat_hex_value

def mac_cat_combinations_generator():
    """
    Generates a list of 4 pairs of mac-cats
    min:0 max:random int
    min:0 max:255
    min:255 max:255
    random min=max
    :return: list
    """
    maccat_hex_value = mac_cat_hex_value_list()
    min_hex = 0x0
    cats = [
        [min_hex, random.choice(maccat_hex_value)],
        [min_hex, maccat_hex_value[-1]],
        [maccat_hex_value[-1], maccat_hex_value[-1]]
    ]
    rand = random.choice(maccat_hex_value)
    cats.append([rand, rand])
    return cats

def mac_cat_invalid_generator():
    """
    Generates a list of 2 pairs of mac-cats
    min:random max:0
    min:random max<min
    :return: list
    """
    maccat_hex_value = mac_cat_hex_value_list()
    min_hex = 0x0
    cats = [[random.choice(maccat_hex_value), min_hex]
            ]
    rand = [random.choice(maccat_hex_value), random.choice(maccat_hex_value)]
    while rand[0] <= rand[1]:
        rand = [random.choice(maccat_hex_value), random.choice(maccat_hex_value)]
    cats.append(rand)
    return cats


def valid_name_generator():
    """Generates valid domain user name
    :return: str
    """
    # Generate one-character name and a name with all digits '_' and ' '.
    max_length = 31
    valid_chars = string.ascii_lowercase + string.digits + '_' + '-'
    length = random.randint(1, max_length - 1)
    # First character must be ASCII lowercase.
    name = random.choice(string.ascii_lowercase)
    while len(name) <= length:
        name = name + random.choice(valid_chars)
    return name


def valid_hostname_generator():
    """Generate the list of valid hostnames. Return list."""
    max_length = 31
    names = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_lowercase) + string.digits + '-'
    ]
    valid_chars = string.ascii_lowercase + string.digits + '-'
    # Create a name with max length.
    long = random.choice(string.ascii_lowercase)
    while len(long) <= max_length - 1:
        long = long + random.choice(valid_chars)
    names.append(long)
    # Create some valid random names.
    while len(names) < 6:
        length = random.randint(1, max_length - 1)
        # First character must be ASCII lowercase.
        name = random.choice(string.ascii_lowercase)
        while len(name) <= length:
            name = name + random.choice(valid_chars)
        names.append(name)
    return names
