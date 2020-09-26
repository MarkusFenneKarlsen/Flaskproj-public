from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    useremail = db.Column(db.String(120), unique=True, nullable=False)
    useraddr = db.Column(db.String(200), nullable=False)
    userpwd = db.Column(db.String(60), nullable=False)
    usertlf = db.Column(db.Integer(), unique=True,  nullable=False)
    accounts = db.relationship('Account',  backref='holder', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.useremail}', '{self.useraddr}', '{self.usertlf}', '{self.accounts}')"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accname = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float)
    accuser = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"account('{self.balance}', '{self.accuser}')"


def createaccs(user):
    acc1 = Account(accname="Brukerkonto", balance=10000, accuser=user)
    acc2 = Account(accname="Sparekonto", balance=100000, accuser=user)
    db.session.add(acc1)
    db.session.add(acc2)
    db.session.commit()
