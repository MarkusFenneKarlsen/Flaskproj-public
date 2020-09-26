Installerte extensions i virtualenv:

installer via pip install


flask
flask-SQLalchemy
flask-bcrypt
flask-wtf
flask-login
flask-limiter
email_validator
phonenumbers

For å tømme database:

Åpne terminal:

>>> from app import db

>>> db.drop_all()

>>> db.create_all()
