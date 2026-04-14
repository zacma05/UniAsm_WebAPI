import secrets
import pyodbc
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DATPHUNG;DATABASE=Fruitables;Trusted_Connection=yes'
conn = pyodbc.connect(cn_str)

#lưu danh sách các token để authorize về sau
tokens = {}

# login
@app.route("/login")
def register_page():
    return render_template("login.html")


# register
@app.route("/register", methods=["POST", "GET"])
def login_page():
    try:
        if request.method == "GET":
            return render_template("register.html")
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        phone = data.get("phone")
        address = data.get("address")

        cursor = conn.cursor()

        #kiem tra xem có tài khoản nào trùng tên chưa
        cursor.execute(
            "SELECT AccountID FROM tblAccount WHERE UserName = ? ",
            (username,)
        )

        if cursor.fetchone():
            return jsonify({"error": "Tên người dùng đã tồn tại"}), 409

        
        cursor.execute(
            "INSERT INTO tblAccount "
            "(UserName, Passwd, UserAddress, Phone, AccountRole) " \
            "VALUES ( ? , ? , ? , ? , 'USER');", (username, password, address, phone)
        )
        conn.commit()
        
        # lay ra id của tài khoản vừa tạo rồi gán token cho nó
        cursor.execute(
            "SELECT AccountID FROM tblAccount WHERE UserName = ? AND Passwd = ?",
            (username, password)
        )

        row = cursor.fetchone()

        token = secrets.token_hex(32)
        tokens[token] = row[0]

        return jsonify({
            "message": "register success",
            "token": token,
            "user": row[0]
        })
    except Exception as e:         
        print(e)
        return str(e), 500
    
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    cursor = conn.cursor()
    cursor.execute(
        "SELECT AccountID FROM tblAccount WHERE UserName = ? AND Passwd = ?",
        (username, password)
    )

    row = cursor.fetchone()

    if not row:
        return jsonify({"error": "Sai tài khoản"}), 401

    token = secrets.token_hex(32)
    tokens[token] = row[0]

    return jsonify({
        "message": "login success",
        "token": token,
        "user": row[0]
    })

@app.route("/cart")
def cart_page():
    return render_template("cart")



@app.route('/product/getProductsByCate', methods=['GET'])
def get_products():
    # Lấy tham số 'cat' từ URL
    category = request.args.get('cat')

    cursor = conn.cursor()
    
    if category:
        query = "SELECT ProductID, ProductName, Category, Price, ProductImage FROM tblProduct WHERE Category = ?"
        cursor.execute(query, (category,))
    else:
        query = "SELECT ProductID, ProductName, Price, Category, ProductImage FROM tblProduct"
        cursor.execute(query)
    
    rows = cursor.fetchall()

    products = [{"id": r[0], "name": r[1], "price": r[2], "category": r[3], "image": r[4]} for r in rows]
    return jsonify(products)
    
@app.route("/shop")
def route_page():
    return render_template("shop.html")


# API lấy danh sách sản phẩm cho file shop.js của bạn
# API lấy danh sách sản phẩm
@app.route("/product/getAllProducts", methods=["GET"])
def get_all_products():
    cursor = conn.cursor()
    
    cursor.execute("SELECT ProductID, ProductName, Category, Price, Stock, Descript, Discount, ProductImage FROM tblProduct")
    
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "ProductID": row[0],
            "ProductName": row[1],
            "Category": row[2],
            "Price": float(row[3]), 
            "Stock": row[4], 
            "Descript": row[5],
            "Discount": row[6],    
            "ProductImage": row[7]
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
