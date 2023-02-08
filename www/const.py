import re

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')  # 邮箱格式验证
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')  # 密码格式验证
COOKIE_NAME = 'awesession'
_COOKIE_KEY = 'Awesome'
