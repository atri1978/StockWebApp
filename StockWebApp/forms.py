from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, ValidationError, IntegerField
from wtforms.validators import Email

class LoginInForm(FlaskForm):
    """Form for loginning in"""

    username = StringField(label="Username", validators=[validators.DataRequired(),
                                                     validators.Length(min=4, max=25)])
    password = PasswordField(label="Password", validators=[validators.DataRequired(),
                                                     validators.Length(min=4, max=25)])
    


class CreateAccountform(FlaskForm):
    """Form for creating account"""

    username = StringField(label="Username", validators=[validators.DataRequired(),
                                                     validators.Length(min=4, max=25)])
    password = PasswordField(label="Password", validators=[validators.DataRequired(),
                                                     validators.Length(min=4, max=25)])
    password_confirm = PasswordField(label="Confirm Password", validators=[validators.EqualTo('password'),
                                                                     validators.DataRequired(),
                                                                     validators.Length(min=4,max=25)])


class StockTradingform(FlaskForm):

    stockSymbol = StringField(label="Symbol", 
                              validators=[validators.DataRequired(message="Please enter a value"),
                                            validators.Length(max=7, message="Not valid symbol")])
    
class UserTradingform(FlaskForm):
    stockSymbol = StringField(label="Stock Symbol",
                              validators=[validators.DataRequired(message="Please enter a value"),
                                          validators.Length(max=7, message="Please enter valid symbol")])
    numberOfShares = IntegerField(label="Amount of shares",
                                  validators=[validators.DataRequired("Amount of shares needed"),
                                              validators.NumberRange(min=1, max=500, message="Can only buy shares between 0-500")])
    

