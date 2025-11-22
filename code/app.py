from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///unisupply.db")




@app.route('/home')
@login_required
def index():
	return render_template("index.html")

@app.route('/seller',methods = ["GET","POST"])
@login_required
def seller():
	if request.method == "GET":
		return render_template("index_seller.html")
	elif request.method == "POST":
		
		name = request.form.get("name")
		price = request.form.get("price")
		phone = request.form.get("phone")
		description = request.form.get("description")
		delivery = request.form.get("flexRadioDefault")

		db.execute("INSERT INTO products (name,price,phone,delivery,description,user_id) VALUES(?,?,?,?,?,?)",name,price,phone,delivery,description,session["user_id"])

		return redirect('/history')

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":

        
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        status = request.form.get("status")
        if len(rows) != 0:
            flash("Username Exists","info")
            return render_template("register.html")
       
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match","info")
            return render_template("register.html")

        hashed_password = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")
        school = request.form.get("school")
        db.execute(
            "INSERT INTO users (username,hash,school,status) VALUES(?,?,?,?)", username, hashed_password,school,status)
        session["user_id"] = db.execute(
            "SELECT id FROM users WHERE username = ?", username
        )[0]["id"]
        if status == '1':
        	return redirect("/purchase")
        else:
        	return redirect("/seller")

@app.route("/direct", methods=["GET","POST"])
@login_required
def direct():
    if request.method == "POST":
        return redirect('/purchase')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        try:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            # User reached route via GET (as by clicking a link or via redirect)
            status = db.execute("SELECT status FROM users WHERE username = ?",request.form.get("username"))
            status = status[0]
            status = status.get("status")
            if status == '1':
                return redirect('/purchase')
            else:
                return redirect('/seller')
        except Exception:
            flash("Invalid username and/or password","info")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def estimate_ingredient_amount(serving_size, num_servings):
    # Calculate total amount needed
    total_amount_needed = serving_size * num_servings
    
    # Determine quantity per unit
    quantity_per_unit = 5
    
    # Calculate number of units needed
    num_units_needed = total_amount_needed / quantity_per_unit
    
    # Round up to the nearest whole unit
    num_units_needed = round(num_units_needed,1)
    
    return num_units_needed



@app.route('/quantity',methods = ["GET","POST"])
def quantity():
	if request.method == "GET":
		return render_template("quantity.html")
	else:
		serving_size = int(request.form.get("serving_size"))
		num_servings = float(request.form.get("num_servings"))
		
		value = estimate_ingredient_amount(serving_size, num_servings)
		return render_template("quantitied.html", value = value)


@app.route('/purchase',methods = ["GET","POST"])
@login_required
def purchase():
    if request.method == "GET":
        products = db.execute("SELECT * FROM products")
        return render_template("purchase.html",products = products)
    else:
        item_id = request.form.get("item_id")

        item = db.execute("SELECT * FROM cart WHERE cart_id = ?",item_id)

        if len(item) > 0:
            flash("Item already in cart","info")
        else:
            db.execute("INSERT INTO cart (cart_id,user_id) VALUES(?,?)",item_id,session["user_id"])

        products = db.execute("SELECT * FROM products")
        return render_template("purchase.html",products = products)


@app.route('/history',methods = ["GET"])
@login_required
def history():
    if request.method == "GET":
        products = db.execute("SELECT * FROM products WHERE user_id = ?",session["user_id"])
        return render_template("history.html",products = products)

@app.route('/delete',methods = ["GET","POST"])
@login_required
def delete():
    if request.method == "POST":
        item = request.form.get("name")
        db.execute("DELETE FROM products WHERE name = ? AND user_id = ?",item,session["user_id"])

        return redirect('/history')


@app.route('/cart',methods = ["GET","POST"])
@login_required
def cart():
    cart_items = db.execute("SELECT * FROM products WHERE product_id IN (SELECT cart_id FROM cart WHERE user_id = ?)",session["user_id"])
    return render_template("cart.html",cart_items = cart_items)


@app.route('/remove',methods = ["GET","POST"])
@login_required
def remove():
    if request.method == "POST":
        id = request.form.get("id")
        remove = db.execute("DELETE FROM cart WHERE cart_id = ? AND user_id = ?",id,session["user_id"])
        items = db.execute("SELECT cart_id FROM cart")
        
        return redirect('/cart')

@app.route('/payed',methods = ["GET","POST"])
@login_required
def payed():
    if request.method == "POST":
        db.execute("DELETE FROM cart WHERE user_id = ?",session["user_id"])
        flash("Payed! Your order will be delivered soon.","info")
        return render_template("cart.html")


@app.route('/',methods=["GET","POST"])
def home():
    if session.get("user_id") is None:
        return render_template("home.html")
    else:
        return render_template("login.html")
