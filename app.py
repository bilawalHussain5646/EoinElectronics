from flask import Flask, flash, request, render_template, redirect, url_for, session, g
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import seed
import schema
import os


# Flask application is created
app = Flask(__name__)

# Application secret key
app.secret_key = "Don't tell anyone"


# EMAIL SMTP DETAILS
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "legendbest123@gmail.com"
app.config['MAIL_PASSWORD'] = "sefnbvaevoctmmav"
app.config['MAIL_DEFAULT_SENDER'] = "legendbest123@gmail.com"
app.config['MAIL_ASCII_ATTACHMENTS'] = False
# These are our application smtp settings so we can send to relevent professor

mail = Mail(app)
# Created Main() for sending mail

# Route: HomePage
# Description: Items will be displayed in this route
# Status: 

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if 'email' in session:     
        if request.method == "GET":          # if Email is already in session
            g.email = session['email']        # Then store it in g
            # fetch products
            products = seed.FetchProducts()
            # render homepage route
            return render_template('homepage.html',session=session,products = products)
        elif request.method == 'POST':      # When a post request is send to the homepage
            
                
            # It will check the action if the action is add-cart
                
            # Email will be requested from the form and stored in email variable
            product_id = request.form['action']
            productName,productPrice = seed.FetchProduct(product_id,)
            
                    
            # Item Name and Item Price are send to the table add-cart
                    
            # send it to InsertAddCart method where our backend will store data if valid it will send True else False
            resp = seed.InsertAddCart(product_id,productName,productPrice, session['email'])
            if (resp):        # if resp is True 
            # And Redirect it to homepage route
                flash("Item added to cart!","success")
                return redirect(url_for('homepage'))
            else:     # Else
                # Show message that Item failed to added in cart
                flash("Item not added in cart", "danger")
                # And redirect to homepage again
                return redirect(url_for('homepage'))
        else:
            flash("Login your Account!","warning" )
            return redirect(url_for("login"))
    elif request.method == "POST":
        flash("Login to your account first ! ","warning")
        return redirect(url_for('login')) 
    else:  # Else
        products = seed.FetchProducts()  # Fetch products
        return render_template("homepage.html",products = products)    # render homepage



# Route: Login
# Description: Login Features are set in this route
# Status : Completed
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:               # if Email is already in session
        g.email = session['email']        # Then store it in g
        # And redirect it to contact_info route
        return redirect(url_for('homepage'))

    elif request.method == 'POST':      # When a post request is send to the login page
        # It will check the action if the action is login
        if (request.form['action'] == 'login'):
            # Email will be requested from the form and stored in email variable
            email = request.form['email']
            # Password is requested and stored in password field
            password = request.form['password']
            # send it to checkRecord method where our backend will check whether our login information is valid or invalid if valid it will send True else False
            resp = seed.CheckRecord(email, password)
            if (resp):        # if resp is True
                session['email'] = email  # Store the email in session

                # And Redirect it to contact_info route
                return redirect(url_for('homepage'))
            else:     # Else
                # Show message that Email or password is invalid
                flash("Email or Password is invalid", "danger")
                # And redirect to login again
                return redirect(url_for('login'))
    else:  # Else
        return render_template("login.html")    # render login page


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Sign up Route
# Description: Add and display sign up form
# Status : Completed


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if 'email' in session:
        g.email = session['email']
        return redirect(url_for('homepage'))

    elif request.method == 'POST':

        if (request.form['action'] == 'signup'):

            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            if (password == confirmPassword):
                password = generate_password_hash(password)
                email = request.form['email']

                resp = seed.InsertRecord(email, password)
                if (resp):
                    flash("Account Created Successfully", "success")
                    return redirect(url_for('signup'))
                else:
                    flash("Use another email", "danger")
                    return redirect(url_for('signup'))
            else:
                flash("Password doesn't matched", "danger")
                return redirect(url_for('signup'))

    else:
        return render_template("signup.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Cart
# Description: Purchasing Items will be done in this route
# Status : 


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'email' in session:
        g.email = session['email']
        if request.method == 'POST':
            if(request.form['action'] == 'BuyItems'):
                email = session['email']
                # for storing data into Database
                resp = seed.PurchaseItems(email)
                if (resp):
                    flash("Item Successfully Purchased", "success")
                    return redirect(url_for('homepage'))
                else:
                    flash("Failed to purchase items", "danger")
                    return redirect(url_for('homepage'))

            else:
                flash("You are trying to access the page without permission", "danger")
                return redirect(url_for('homepage'))

        else:
            # Fetch cart data from cart table
            cartinfo,Total = seed.FetchCart(session['email'])

            # send data to cart page
            return render_template('cart.html',cartinfo=cartinfo,Total=Total)
    else:
        flash("Session Ended", "warning")
        return redirect(url_for('login'))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response



# Route: Logout
# Description: Logout the account
# Status : Completed


@ app.route("/logout")
def logout():
    if 'email' in session:
        session.pop('email', None)
        flash("Account Logged Out", "success")
        return redirect(url_for('homepage'))
    else:
        flash("Session Ended", "danger")
        return redirect(url_for('login'))


@ app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


app.debug = True


if __name__ == '__main__':
    app.run(port=3000, debug=True)
