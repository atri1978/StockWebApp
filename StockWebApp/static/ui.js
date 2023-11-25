logInButton = $("#login-button-nav");
logOutButton = $("#logout-button-nav");
getStartedButton = $("#button")
logInreturnButton = $("#return-button")
dayGraphButton = $("h4#stockH3")
GraphButton1 = $("h4#stock1")
GraphButton2 = $("h4#stock2")
GraphButton3 = $("h4#stock3")
weekGraphButton = $("h3#stockH3")
article = $("#article");
articleLocation = $("a#articleLocation")
sellButton = $("#sellshares-button")
buyButton = $("#buyshares-button")



sellButton.click(function(){
    location.href = ("/sell")
})

buyButton.click(function(){
    location.href = ("/buy")
})

getStartedButton.click(function(){
location.href = ("/createAccount")
})

logInButton.click(function(){
    location.href = ("/login")
})

logOutButton.click(function(){
    location.href = ("/logout")
})

logInreturnButton.click(function(){
    location.href = ("/")
})

dayGraphButton.click(function(){
    location.href = ("/daygraph")
})


GraphButton1.click(function(){
    location.href = ("/graph1")
})

GraphButton2.click(function(){
    location.href = ("/graph2")
})

GraphButton3.click(function(){
    location.href = ("/graph3")
})

weekGraphButton.click(function(){
    location.href = ("/weekGraph")
})


x = articleLocation.html()
articleInt = x.indexOf("htt")

articleLink = x.slice(articleInt)
articleLocation.attr("href", articleLink)


