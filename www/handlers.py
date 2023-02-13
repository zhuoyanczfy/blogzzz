import hashlib
import json
import logging
import time
from random import randint

from aiohttp import web
import aiotask_context as aiocontext
from www.apis import APIValueError, APIError, Page
from www.common.log.log import logger
from www.common.web.htmltool import get_page_index
from www.common.web.user import user2cookie, check_admin
from www.coroweb import get, post
from www.models import User, Blog, next_id
from www.const import _RE_EMAIL, _RE_SHA1, COOKIE_NAME


@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


@get('/signin')
def signin():
    return {
        '__template__': 'login.html'
    }


@get('/blogs/create')
def manager_blog():
    return {

        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }


@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


@post('/api/authenticate')
async def authenticate(*, email, passwd):
    try:
        if not email:
            raise APIValueError('email', 'Can not find email.')
        if not passwd:
            raise APIValueError('passwd', 'Can not find password.')
        users = await User.findAll('email=?', [email])

        if len(users) == 0:
            raise APIValueError('email', 'Email not exist.')
        user = users[0]
        # check passwd:
        sha1 = hashlib.sha1()
        sha1.update(user.id.encode('utf-8'))
        sha1.update(b':')
        sha1.update(passwd.encode('utf-8'))
        if user.passwd != sha1.hexdigest():
            raise APIValueError('passwd', f'user:{user.name} Invalid password.')
        # authenticate ok, set cookie:
        r = web.Response()
        r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
        user.passwd = '******'
        r.content_type = 'application/json'
        r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')

        logger.info(f"user:{user.name} log in")
        return r
    except APIValueError as e:
        logger.error(e)



@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logger.info('user signed out.')
    return r


@get('/api/user')
async def get_all_users(request):
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = "*******"
    return dict(users=users)


@post('/api/user/create')
async def create_user(*, email, password, name):
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError(email)
    if not name or not name.strip():
        raise APIValueError(name)
    if not password or not _RE_SHA1.match(password):
        raise APIValueError(password)
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, password)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
                image='https://dn-qiniu-avatar.qbox.me/avatar/%s?d=mm&s=120' % hashlib.md5(
                    email.encode('utf-8')).hexdigest())
    await user.save()
    logger.info(f"create user successful! username:{user.name}")
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@get('/api/blogs')
async def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


@get('/api/blogs/{id}')
async def api_get_blog(*, id):
    blog = await Blog.find(id)
    return blog


@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


@get('/')
async def index1(request):
    # aiocontext.set(key="view_mark", value=str(randint(10 ** 11, 10 ** 12)))
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time() - 120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time() - 7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }
