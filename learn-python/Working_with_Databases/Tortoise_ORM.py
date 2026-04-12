# Tortoise ORM: Async ORM

from tortoise import Tortoise, fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    age = fields.IntField()

async def run():
    await Tortoise.init(
        db_url='sqlite://example.db',
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()

    # Add a new user
    await User.create(name='Alice', age=30)

    # Query users
    users = await User.all()
    for user in users:
        print(user.name, user.age)

import asyncio
asyncio.run(run())
