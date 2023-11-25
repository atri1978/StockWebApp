
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(UserMixin, db.Model):
    """Users"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.String,
                         nullable = False,
                         unique = True)

    password = db.Column(db.String,
                         nullable =False)
    
    def get_id(self):
        return super().get_id()
    

class Stock(UserMixin, db.Model):
    """ Users stock data"""

    __tablename__ = "stocks"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)

    username = db.Column(db.Integer,
                       nullable = False)
    
    stock = db.Column(db.String,
                          nullable = False,
                          unique = True)
    
    numShares = db.Column(db.Integer,
                        nullable = False)
    

    


class UserPortfolio(UserMixin, db.Model):

    __tablename__ = "user_portfolio"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)

    username = db.Column(db.Integer,
                       nullable = False)
    
    profit = db.Column(db.NUMERIC,
                        nullable = False)
    
    moneyLeft = db.Column(db.NUMERIC,
                        nullable = True
                        )