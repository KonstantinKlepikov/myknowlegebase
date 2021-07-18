# sqlalchemy deleting

[Основная статья](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#deleting)

Существует нюанс, связанный с удалением данных.

```python
>>> from sqlalchemy.orm import joinedload

SQL>>> jack = session.query(User).\
...                        options(joinedload(User.addresses)).\
...                        filter_by(name='jack').one()
>>> jack
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>

>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]

>>> session.delete(jack)
SQL>>> session.query(User).filter_by(name='jack').count()
0

>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
...  ).count()
2
```

В данном случае, хотя мы удалили пользователя, связанные с ним адреса остались. Чтобы удалять связанные объекты в других таблицах, необходимо прописать каскад в модели

```python
>>> class User(Base):
...     __tablename__ = 'users'
...
...     id = Column(Integer, primary_key=True)
...     name = Column(String)
...     fullname = Column(String)
...     nickname = Column(String)
...
...     addresses = relationship("Address", back_populates='user',
...                     cascade="all, delete, delete-orphan")
...
...     def __repr__(self):
...        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
...                                self.name, self.fullname, self.nickname)

>>> class Address(Base):
...     __tablename__ = 'addresses'
...     id = Column(Integer, primary_key=True)
...     email_address = Column(String, nullable=False)
...     user_id = Column(Integer, ForeignKey('users.id'))
...     user = relationship("User", back_populates="addresses")
...
...     def __repr__(self):
...         return "<Address(email_address='%s')>" % self.email_address
```

Теперь все прошло как надо (в примере вначале снесли один из адресов).

```python
# load Jack by primary key
SQL>>> jack = session.query(User).get(5)

# remove one Address (lazy load fires off)
SQL>>> del jack.addresses[1]

# only one address remains
SQL>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
1

>>> session.delete(jack)

SQL>>> session.query(User).filter_by(name='jack').count()
0

SQL>>> session.query(Address).filter(
...    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
0
```

[[sqlalchemy]]
[[sqlalchemy-querying]]
