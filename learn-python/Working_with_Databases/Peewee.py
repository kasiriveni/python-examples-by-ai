# Peewee: Lightweight ORM

from peewee import SqliteDatabase, Model, CharField, IntegerField

db = SqliteDatabase('example.db')

class User(Model):
    name = CharField()
    age = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([User])

# Add a new user
user = User.create(name='Alice', age=30)

# Query users
for user in User.select():
    print(user.name, user.age)
