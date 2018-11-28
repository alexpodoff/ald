create_user = {
    '01-padmin': "Введите пароль администратора ALD:",
    '02-puser': "Введите новый пароль для пользователя '%s':",
    '03-prepeat': "Повторите пароль:",
    '04-uid': "Введите идентификатор пользователя \(UID\) \[[0-9]+\]:",
    '05-gcreate': "Создать новую первичную группу .* \[yes\]:",
    '06-group': "Введите имя новой первичной .* \[%s\]:",
    '07-gid': "Введите идентификатор группы \(GID\) \[[0-9]+\]:",
    '08-gdesc': "Введите описание группы .*:",
    '09-shell': "Введите командную оболочку .* \[/bin/bash\]:",
    '10-fstype': "Введите тип ФС .* local, nfs, cifs\):",
    '11-fserv': "Введите сервер домашнего каталога .*:",
    '12-homedir': "Введите домашний .*\[/ald_home/%s\]: ",
    '13-fname': "Введите полное имя пользователя \[%s\]:",
    '14-gecos': "Введите параметр GECOS .*\[%s,,,\]:",
    '15-udesc': "Введите описание пользователя:",
    '16-policy': "Введите политику пароля для пользователя \[default\]:",
    '17-chpass': "Установить флаг .*\(yes/no\) \[no\]:",
    '18-correct': "Всё правильно\? \(yes/no\) \[no\]:"
}

create_user_parametrize = {
    'gecos': "fake,gecos,for,user",
    'home': "/home/fake",
    'home-type': "local",
    'user-desc': "fakedesk",
    'login-shell': "/bin/sh",
    'full-name': "'Full Users Name'",
    'group': 'fakegroup',
    'group-desc': 'fakegdesk'
}

create_hgroup = {
    '01-padmin': "Введите пароль администратора ALD:",
    '02-desc': "Введите описание группы компьютеров:"
}

modify_hgroup = {
    'name': "new_name",
    'hgroup-desc': "new_desc",
}

del_hgroup = {
    '01-padmin': "Введите пароль администратора ALD:",
    '02-confirm': "Продолжить\? \(yes/no\) \[no\]:"
}

modify_user = {
    'gecos': "fake,gecos,for,user",
    'home': "/home/fake",
    'home-type': "local",
    'user-desc': "fakedesk",
    'login-shell': "/bin/sh",
    'full-name': "'Full Users Name'"
}

del_user = {
    '01-padmin': "Введите пароль администратора ALD:",
    '02-confirm': "Продолжить\? \(yes/no\) \[no\]:",
    '03-gconfirm': "Удалить группу\? \(yes/no\) \[yes\]:"
}

create_policy = {
    '01-padmin': "Введите пароль администратора ALD:",
    '02-maxttl': "\(в формате NNd или NNh или NNm\) \[infinite\]:",
    '03-minttl': "\(в формате NNd или NNh или NNm\) \[infinite\]:",
    '04-lenght': "Введите минимальную длину пароля \[8\]:",
    '05-class': "используемых в пароле \[3\]:",
    '06-oldpass': "сохраняемых для истории \[5\]:"
}

modify_policy = {
    'max-life': "50d",
    'min-life': "10d",
    'min-length': "5",
    'min-classes': "2"
}

del_policy = {
    '01-padmin': "Введите пароль администратора ALD:",
    '02-confirm': "Продолжить\? \(yes/no\) \[no\]:"
}

create_host = {
    '01-padmin': "Введите пароль администратора ALD:",
    '02-desc': "Введите описание компьютера:",
    '03-confirm': "Всё правильно\? \(yes/no\) \[no\]:"
}

modify_host = {
    'host-desc': "testdeck",
    'host-flags': "[PCFD]",
    'server-id': "99"
}

del_host = {
    '01-padmin': "Введите пароль администратора ALD:",
    '02-confirm': "Продолжить\? \(yes/no\) \[no\]:"
}

create_maclev = {
    '01-padmin': "Введите пароль администратора ALD:"
}

del_maclev = {
    '01-padmin': "Введите пароль администратора ALD:",
    '02-confirm': "Продолжить\? \(yes/no\) \[no\]:"
}

aud_flags = {
    'open': 1,
    'create': 2,
    'exec': 4,
    'delete': 8,
    'chmod': 16,
    'chown': 32,
    'mount': 64,
    'module': 128,
    'uid': 256,
    'gid': 512,
    'audit': 1024,
    'acl': 2048,
    'mac': 4096,
    'cap': 8192,
    'chroot': 16384,
    'rename': 32768,
    'net': 65536
}
