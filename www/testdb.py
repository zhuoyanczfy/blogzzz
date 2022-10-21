import asyncio

import orm
from models import User, Blog, Comment


async def test(loop):
    await orm.create_pool(loop, user='root', password='root', db='awesome')

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    testdict = User(name = "Test")

    print(u.get("created_at"))

    #await u.save()
    #userdict = await  User.findAll(where="name = \"Test\"")

    #for user in userdict:
    #    print(user)

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
