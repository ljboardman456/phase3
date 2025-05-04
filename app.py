from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# DB config
conn = psycopg2.connect(
    dbname="restaurant_db",
    user="your_db_user",
    password="your_db_password",
    host="localhost",
    port="5432"
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cur = conn.cursor()
    cur.execute("SELECT id, role_id FROM Users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    if user:
        session['user_id'] = user[0]
        session['role_id'] = user[1]
        return redirect('/dashboard')
    else:
        return "Invalid credentials"

@app.route('/dashboard')
def dashboard():
    if 'role_id' not in session:
        return redirect('/')
    role_id = session['role_id']
    if role_id == 1:
        return render_template('admin_dashboard.html')
    elif role_id == 2:
        return render_template('manager_dashboard.html')
    elif role_id == 3:
        return render_template('staff_dashboard.html')
    else:
        return "Access denied"

@app.route('/admin/add_menu', methods=['POST'])
def add_menu():
    if session.get('role_id') != 1:
        return "Unauthorized"
    name = request.form['name']
    category = request.form['category']
    description = request.form['description']
    price = request.form['price']
    cur = conn.cursor()
    cur.execute("SELECT add_menu_item(%s, %s, %s, %s)", (name, category, description, price))
    conn.commit()
    return redirect('/dashboard')

@app.route('/staff/generate_bill/<int:order_id>')
def generate_bill(order_id):
    if session.get('role_id') != 3:
        return "Unauthorized"
    cur = conn.cursor()
    cur.execute("SELECT generate_bill(%s)", (order_id,))
    conn.commit()
    return "Bill generated"

if __name__ == '__main__':
    app.run(debug=True)
