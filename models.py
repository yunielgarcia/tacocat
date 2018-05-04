from peewee import *
import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('taco.db')


class User(UserMixin, Model):  # From more to less specific
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)  # no now() otherwise will have the date when the file

    class Meta:
        database = DATABASE
        # And since order_by is a tuple (you can use a list if you want),
        # we have to include that trailing comma if there's only one tuple member.
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password)
                )
        except IntegrityError:  # Meaning a field already exits
            raise ValueError("User already exists")


class Taco(Model):
    protein = CharField(max_length=100, default='')
    shell = CharField()
    cheese = BooleanField(default=False)
    extras = TextField()
    timestamp = DateTimeField(
        default=datetime.datetime.now)
    user = ForeignKeyField(
        # rel_model=User,
        # related_name='tacos'
        model=User,
        backref='tacos'
    )

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()

