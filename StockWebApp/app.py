from flask import Flask, redirect, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from forms import *
from models import *
from middleware import *
import pyautogui as pag
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from datetime import timedelta




app = Flask(__name__)
# the toolbar is only enabled in debug mode:
app.debug = True
# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stockdatabase'
app.config['SLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SECRET'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.permanent_session_lifetime = timedelta(minutes=5)


login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

toolbar = DebugToolbarExtension(app)
connect_db(app)





@app.route("/")
def home():
    return render_template("home.html")

@app.route("/retry")
def retry():
    return render_template("retryError.html")

@app.route("/portfolio")
@login_required
def portfolio_view():
    try:
        id = current_user.get_id()
        profit = db.session.query(UserPortfolio.profit).filter(UserPortfolio.username==id).first()._data[0]
        money = db.session.query(UserPortfolio.moneyLeft).filter(UserPortfolio.username==id).first()._data[0]
        roundedmoney = round(money,2)
        numStocks = db.session.query(Stock.stock).filter(Stock.username==id).count()
        topStocks = db.session.query(Stock.stock).filter(Stock.username==id).order_by(Stock.numShares.desc()).limit(3).all()
        stock1 = topStocks[0][0]
        stock2=topStocks[1][0]
        stock3=topStocks[2][0]
        session.permanent = True  
        news1 = get_newsStock(stock_symbol=stock1)
        if session.get("data") is None:
            data1 = getData(stock1)
            data2 = getData(stock2)
            data3 = getData(stock3)

            session["data"] = data1
            session["data2"] = data2
            session["data3"] = data3
        else:
            try:
                data1 = getData(stock1)
                data2 = getData(stock2)
                data3 = getData(stock3)
            except:
                data1 = session["data"]
                data2 = session["data2"]
                data3 = session["data3"]
        dfAnalysis1 = dataframeAnalysis(data1)
        dfMax1 = dfAnalysis1["max"]
        dfMin1 = dfAnalysis1["min"]
        dfPChange1 = dfAnalysis1["percentChange"]
        createGraphstock1(stock1)

        news2 = get_newsStock(stock_symbol=stock2)  
        dfAnalysis2 = dataframeAnalysis(data2)
        dfMax2 = dfAnalysis2["max"]
        dfMin2 = dfAnalysis2["min"]
        dfPChange2 = dfAnalysis2["percentChange"]
        createGraphstock2(stock2)

        news3 = get_newsStock(stock_symbol=stock3)
        dfAnalysis3 = dataframeAnalysis(data3)
        dfMax3 = dfAnalysis3["max"]
        dfMin3 = dfAnalysis3["min"]
        dfPChange3 = dfAnalysis3["percentChange"]
        createGraphstock3(stock3)

        return render_template("portfolio.html", profit=profit, roundedmoney=roundedmoney, numStocks=numStocks,
                            stock1=stock1, news1=news1,data1 = data1,dfAnalysis1= dfAnalysis1,dfMax1=dfMax1,dfMin1=dfMin1,dfPChange1=dfPChange1,
                            stock2 =stock2, news2=news2,data2 = data2,dfAnalysis2= dfAnalysis2,dfMax2=dfMax2,dfMin2=dfMin2,dfPChange2=dfPChange2,
                            stock3 = stock3, news3=news3,data3 = data3,dfAnalysis3= dfAnalysis3,dfMax3=dfMax3,dfMin3=dfMin3,dfPChange3=dfPChange3
                            )
    except:
        return redirect("/retry")



@app.route("/stock", methods=["GET", "POST"])
@login_required
def trading_view():
    try:
        form = StockTradingform()

        if form.validate_on_submit():
            stockSymbol = form.stockSymbol.data
            
            news = get_news(stock_symbol=stockSymbol)
            data = getData(stockSymbol)
            dfAnalysis = dataframeAnalysis(data)
            dfMax = dfAnalysis["max"]
            dfMin = dfAnalysis["min"]
            dfPChange = dfAnalysis["percentChange"]
            dfCurrent = dfAnalysis["currentVal"]
            dfInitial = dfAnalysis["intialVal"]
            createGraph(stockSymbol)

            weekdata = weekData(stockSymbol)
            weekdfAnalysis = dataframeAnalysis(weekdata)
            weekdfMax = weekdfAnalysis["max"]
            weekdfMin = dfAnalysis["min"]
            weekdfPChange = weekdfAnalysis["percentChange"]
            weekdfCurrent = weekdfAnalysis["currentVal"]
            weekdfInitial = weekdfAnalysis["intialVal"]
            weekGraph(stockSymbol)
            return render_template("tradingStock.html",stockSymbol = stockSymbol,
                                    dfMax = dfMax, 
                                    dfMin = dfMin,
                                    dfPChange = dfPChange,
                                    dfCurrent = dfCurrent,
                                    dfInitial = dfInitial,
                                    weekdfMax = weekdfMax,
                                    weekdfMin = weekdfMin,
                                    weekdfPChange = weekdfPChange,
                                        weekdfInitial = weekdfInitial,
                                        weekdfCurrent = weekdfCurrent,
                                        news = news)

        else:   
            return render_template("trading.html", form=form)
        
    except:
        return redirect("/retry")
    
@app.route("/daygraph")
def dayGraph_view():
    return render_template("dayGraph.html")

@app.route("/weekGraph")
def weekGraph_view():
    return render_template("weekGraph.html")

@app.route("/graph1")
def graph1():
    return render_template("stock1Graph.html")

@app.route("/graph2")
def graph2():
    return render_template("stock2Graph.html")

@app.route("/graph3")
def graph3():
    return render_template("stock3Graph.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("home.html")

@app.route('/accountError')
def accounterror():
    return render_template("accountError.html" )

@app.route("/trading")
@login_required
def stock_view():
    return render_template("stock.html")
    
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buyStocks():
    """Trading BUY form"""
    form = UserTradingform()

    if form.validate_on_submit():
        stock = form.stockSymbol.data
        shares = form.numberOfShares.data
        username = current_user.get_id()
        addDataStock(stock, shares, username)
        addDataUser(username,stock,shares)

        return render_template("stock.html")
    else:
        return render_template("buystock.html", form=form)
    

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sellStocks():
    """Trading SELL form """
    form = UserTradingform()
    if form.validate_on_submit():
        stock = form.stockSymbol.data
        shares = form.numberOfShares.data
        username = current_user.get_id()
        
        check_shares = db.session.query(
                       Stock.numShares).filter(
                       Stock.username == username,
                       Stock.stock == stock).first()._data[0]
        if shares > check_shares:
    
            return redirect("/stockError")
        
        sellDataStock(stock,shares,username)
        sellDataUser(username,stock,shares)

        return render_template("stock.html")
    else:
        return render_template("sellstock.html", form=form)
    
@app.route('/stockError')
def stockerror():
    return render_template("stockError.html")
    
    


@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))

@app.route("/login", methods=["GET", "POST"])
def logIn():
    """Login Form"""

    form = LoginInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = authUser(username, password)
        if user:
            login_user(user)
            return redirect("/portfolio")
    
    else:
        return render_template("logIn.html", form=form)
    

@app.route("/createAccount", methods=["GET", "POST"])
def createAccount():
    """Create account form"""

    form = CreateAccountform()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if checkUser(username):
            return redirect("/accountError")
    
        else:
            addUser(username, password)
            return redirect("/logIn")

    else:
        return render_template("createAccount.html", form=form)   
    
    
    
    

