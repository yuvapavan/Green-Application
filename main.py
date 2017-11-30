from flask import *
from flask import jsonify
import sqlite3, hashlib, os
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def getLoginDetails():
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = '" + session['email'] + "'")
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM cart WHERE userId = " + str(userId))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)

@app.route("/")
def root():
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    return json.dumps({'itemData':itemData, 'loggedIn':loggedIn, 'firstNam':firstName, 'noOfItem':noOfItems, 'categoryData':categoryData})   
    #return render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData)



@app.route("/shelters")
def shelters():
    with sqlite3.connect('database297.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT Name,Address,Phone,Latitude,Longitude FROM Shelter')
        itemData = cur.fetchall()
        a = parse(itemData)
        l=[]
        for i in range(0,len(a[0])):
             d={}
             d['Name']=a[0][i][0]
             d['Location']=a[0][i][1]
             d["PhoneNumber"]=a[0][i][2]
             d["latitude"]=a[0][i][3]
             d["longitude"]=a[0][i][4]
             l.append(d)
    return jsonify({'data':l}),{'Content-Type':'application/json'}


@app.route("/emergency")
def emergency():
    with sqlite3.connect('database297.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT Name,Address,Phone FROM Emergency')
        itemData = cur.fetchall()
        a = parse(itemData)
        l=[]
        for i in range(0,len(a[0])):
             d={}
             d['Name']=a[0][i][0]
             d['Address']=a[0][i][1]
             d["PhoneNumber"]=a[0][i][2]
             l.append(d)
    return jsonify({'data':l}),{'Content-Type':'application/json'} 



@app.route("/rescuers")
def rescuers():
    with sqlite3.connect('database297.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT Name,Phone,Latitude,Longitude FROM Rescuer')
        itemData = cur.fetchall()
        a = parse(itemData)
        l=[]
        for i in range(0,len(a[0])):
             d={}
             d['Name']=a[0][i][0]
             d['Phone']=a[0][i][1]
             d["Latitude"]=a[0][i][2]
             d["Longitude"]=a[0][i][3]
             l.append(d)
    return jsonify({'data':l}),{'Content-Type':'application/json'}


@app.route("/victims")
def victims():
    with sqlite3.connect('database297.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT Name,Phone,Latitude,Longitude FROM Victims')
        itemData = cur.fetchall()
        a = parse(itemData)
        l=[]
        for i in range(0,len(a[0])):
             d={}
             d['Name']=a[0][i][0]
             d['Phone']=a[0][i][1]
             d["Latitude"]=a[0][i][2]
             d["Longitude"]=a[0][i][3]
             l.append(d)
    return jsonify({'data':l}),{'Content-Type':'application/json'}  



@app.route("/add")
def admin():
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
    conn.close()
    return json.dumps({'categories':categories})
    #return render_template('add.html', categories=categories)

#Admin Add Functionality
@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        categoryId = int(request.form['category'])

        #Uploading image procedure
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with sqlite3.connect('database235.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO products (name, price, description, image, stock, categoryId) VALUES (?, ?, ?, ?, ?, ?)''', (name, price, description, imagename, stock, categoryId))
                conn.commit()
                msg="added successfully"
            except:
                msg="error occured"
                conn.rollback()
        conn.close()
        print(msg)
        return redirect(url_for('root'))

#Admin Remove Functionality
@app.route("/remove")
def remove():
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        data = cur.fetchall()
    conn.close()
    #return json.dumps({'data':data})
    return json.dumps({'data':data})

@app.route("/removeItem")
def removeItem():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    with sqlite3.connect('database235.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM products WHERE productID = ' + productId)
            conn.commit()
            cur.execute('SELECT productId, name, price, description, image, stock FROM products')
            itemData = cur.fetchall()
            cur.execute('SELECT categoryId, name FROM categories')
            categoryData = cur.fetchall()
            msg = "Deleted successsfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    print(msg)
    itemData = parse(itemData)
    return json.dumps({'itemData':itemData, 'loggedIn':loggedIn, 'firstNam':firstName, 'noOfItem':noOfItems, 'categoryData':categoryData})
    #return redirect(url_for('root'))

#Call API like this 
#http://localhost:5000/displayCategory?categoryId=2
@app.route("/displayCategory")
def displayCategory():
        loggedIn, firstName, noOfItems = getLoginDetails()
        categoryId = request.args.get("categoryId")
        print (categoryId)
        #categoryId = request.args.get(1)
        with sqlite3.connect('database235.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = " + categoryId)
            data = cur.fetchall()
        conn.close()
        categoryName = data[0][4]
        data = parse(data)
        return json.dumps({'data':data, 'loggedIn':loggedIn, 'firstName':firstName, 'noOfItem':noOfItems, 'categoryName':categoryName})
        #return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryName=categoryName)

@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    return json.dumps({'loggedIn':loggedIn, 'firstName':firstName, 'noOfItems':noOfItems})
    #return render_template("profileHome.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = '" + session['email'] + "'")
        profileData = cur.fetchone()
    conn.close()
    return json.dumps({'profileData':profileData, 'loggedIn':loggedIn, 'firstName':firstName, 'noOfItems':noOfItems})
    #return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('database235.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM users WHERE email = '" + session['email'] + "'")
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        with sqlite3.connect('database235.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('editProfile'))


@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else: 
        return json.dumps({'error':None})
        #return render_template('login.html', error='')


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        password = request.args.get('pwd')
        email = request.args.get('em')
        if is_valid(email, password):
            session['email'] = email
            return json.dumps({"OK":200}),{'Content-Type':'application/json'}
        else:
            error = 'Invalid UserId / Password'
            return json.dumps({"invalid":404}),{'Content-Type':'application/json'}

#call APi as
#http://localhost:5000/productDescription?productId=4
@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ' + productId)
        productData = cur.fetchone()
    conn.close()
    #return render_template("productDescription.html", data=productData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)
    return  json.dumps({'data':productData, 'loggedIn':loggedIn, 'firstName':firstName, 'noOfItems':noOfItems})

@app.route("/addToCart")
def addToCart():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = int(request.args.get('productId'))
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        #cur.execute("SELECT userId FROM users WHERE email = '" + session['email'] + "'")
        userId = "mrajesh971"
        try:
            cur.execute("INSERT INTO cart (userId, productId) VALUES (?, ?)", (userId, productId))
            conn.commit()
            cur.execute('SELECT * FROM cart')
            itemData = cur.fetchall()
            cur.execute('SELECT categoryId, name FROM categories')
            categoryData = cur.fetchall()
            msg = "Added successfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    itemData = parse(itemData)
    return json.dumps({'itemData':itemData}) 

@app.route("/cart")
def cart():
    #if 'email' not in session:
    #    return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    #email = session['email']
    #email = "mrajesh971@gmail.com"
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        #cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
        #userId = cur.fetchone()[0]
        #userId="mrajesh971"
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, cart WHERE products.productId = cart.productId AND cart.userId = 'mrajesh971' ")
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return json.dumps({'products':products, 'totalPrice':totalPrice, 'loggedIn':loggedIn, 'firstName':firstName, 'noOfItems':noOfItems})

@app.route("/removeFromCart")
def removeFromCart():
    #if 'email' not in session:
    #       return redirect(url_for('loginForm'))
    #email = session['email']
    productId = int(request.args.get('productId'))
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        #cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
        userId = "mrajesh971"
        try:
            cur.execute("DELETE FROM cart WHERE userId = 'mrajesh971'" +  " AND productId = " + str(productId))
            conn.commit()
            msg = "removed successfully"
            cur.execute("select * from cart")
            cartdetails=cur.fetchall()
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    #return redirect(url_for('root'))
    return json.dumps({'data':cartdetails})

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

def is_valid(email, password):
    con = sqlite3.connect('database235.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        print ("in Post")
        password = request.args.get('pwd')
        email = request.args.get('em')
        firstName = request.args.get('fname')
        lastName = request.args.get('lname')
        address1 = "San Jose"
        address2 = "Cali"
        zipcode = "95113"
        city = "SJ"
        state = "CA"
        country = "USA"
        phone = "123456789"

        with sqlite3.connect('database235.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone))
                con.commit()
                cur.execute('SELECT email, password,firstName,lastName FROM users')
                users=cur.fetchall()
                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        #return render_template("login.html", error=msg)
        return json.dumps({"users":users})

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans



if __name__ == '__main__':
    app.run(debug=True)
