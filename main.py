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




@app.route("/")
def root():
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    return json.dumps({'itemData':itemData})   

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




@app.route("/personalinfo")
def personalinfo():
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT email,uname,mobile,address FROM users where email="naresh@gmail.com"')
        itemData = cur.fetchall()
    a = parse(itemData)
    l=[]
    for i in range(0,len(a[0])):
        d={}
        d['email']=a[0][i][0]             
        d["uname"]=a[0][i][1]
        d["mobile"]=a[0][i][2]
        d['address']=a[0][i][3]
        l.append(d)
    return json.dumps({'itemData':l}),{'Content-Type':'application/json'}

   





@app.route("/stores")
def rescuers():
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT Name,Latitude,Longitude,Phone,Hours FROM Stores')
        itemData = cur.fetchall()
        a = parse(itemData)
        l=[]
        for i in range(0,len(a[0])):
             d={}
             d['Name']=a[0][i][0]             
             d["Latitude"]=a[0][i][1]
             d["Longitude"]=a[0][i][2]
             d['Phone']=a[0][i][3]
             d['Hours']=a[0][i][4]
             l.append(d)
    return jsonify({'data':l}),{'Content-Type':'application/json'}






@app.route("/adminlogin")
def adminrender():
	return render_template('index.html')

@app.route("/terms")
def terms():
	return render_template('termsofuse.html')

@app.route("/help")
def help():
	return render_template('help.html')

@app.route("/privacy")
def policy():
	return render_template('privacypolicy.html')


#For Admin Add Functionality
@app.route("/add")
def admin():
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
    conn.close()
    return render_template('add.html', categories=categories)


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#Admin Add Functionality
@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        description = request.form['description']
        categoryId = int(request.form['category'])
        review= request.form['review']

        # #Uploading image procedure
        # image = request.files['image']
        # if image and allowed_file(image.filename):
        #     filename = secure_filename(image.filename)
        #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = "solar-40"

        with sqlite3.connect('database235.db') as conn:
            try:
                cur = conn.cursor()
                print ("cmg here")
                cur.execute('''INSERT INTO products (name, price, description, image, stock,Review,categoryId) VALUES (?, ?, ?, ?, ?, ?, ?)''', (name, price, description, imagename, stock, review, categoryId))
                print ("here")
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
    return render_template('remove.html', data=data)
    # return json.dumps({'data':data})

#http://localhost:9000/removeItem?productId=18
@app.route("/removeItem")
def removeItem():
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
    print(msg)
    return redirect(url_for('root'))
   

#Call API like this 
#http://localhost:5000/displayCategory?categoryId=2
@app.route("/displayCategory")
def displayCategory():
        #loggedIn, firstName, noOfItems = getLoginDetails()
        categoryId = request.args.get("categoryId")
        print (categoryId)
        with sqlite3.connect('database235.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = " + categoryId)
            data = cur.fetchall()
        conn.close()
        categoryName = data[0][4]
        a = parse(data)
        l=[]
        for i in range(0,len(a[0])):
             d={}
             d['productid']=a[0][i][0]             
             d["name"]=a[0][i][1]
             d["price"]=a[0][i][2]
             d['image']=a[0][i][3]
             d['categories']=a[0][i][4]
             l.append(d)
        return json.dumps({'data':l,'categoryName':categoryName}),{'Content-Type':'application/json'}

        
        


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        password = request.args.get('pwd')
        email = request.args.get('em')
        if is_valid(email, password):
            return json.dumps({"OK":200}),{'Content-Type':'application/json'}
        else:
            error = 'Invalid UserId / Password'
            return json.dumps({"invalid":404}),{'Content-Type':'application/json'}

#call APi as
#http://localhost:5000/productDescription?productId=4
@app.route("/productDescription")
def productDescription():
    productId = request.args.get('productId')
    with sqlite3.connect('database235.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, Review FROM products WHERE productId = ' + productId)
        productData = cur.fetchone()
    conn.close()
    d={}
    d['productId']=productData[0]
    d['name']=productData[1]
    d['price']=productData[2]
    d['description']=productData[3]
    d['image']=productData[4]
    d['Review']=productData[5]

    return  json.dumps({'data':d}),{'Content-Type':'application/json'}



@app.route("/logout")
def logout():
    return json.dumps({"ok":200})

def is_valid(email, pwd):
    con = sqlite3.connect('database235.db')
    cur = con.cursor()
    cur.execute('SELECT email, pwd FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] ==pwd:
            return True
    return False





@app.route('/register', methods = ['POST'])
def api_message():
	pwd=request.json.get("pwd")
	email=request.json.get("email")
	uname=request.json.get("uname")
	mobile=request.json.get("mobile")
	address=request.json.get("address")

	with sqlite3.connect('database235.db') as con:
		try:
			cur = con.cursor()
			cur.execute('INSERT INTO users (pwd, email, uname, mobile, address) VALUES (?, ?, ?, ?, ?)', (pwd, email, uname, mobile, address))
			con.commit()
			msg = "Registered Sucessfully"
		except:
			con.rollback()
			msg = "Error occured"
	con.close()
	return json.dumps({"data":msg}),{'Content-Type':'application/json'}


    
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
    app.run(host='0.0.0.0',port=9000,debug=True)
