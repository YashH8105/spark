from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Initialize the Flask Application
app = Flask(__name__)

# 2. Set a Secret Key
app.secret_key = 'a_very_secret_key_that_should_be_changed'

# 3. Configure the MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'       # Or your database host
app.config['MYSQL_USER'] = 'root'            # Your database username
app.config['MYSQL_PASSWORD'] = '' # Your database password
app.config['MYSQL_DB'] = 'spark'       # The database you created
app.config['MYSQL_PORT'] = 3308 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # Returns rows as dictionaries

# 4. Initialize MySQL
mysql = MySQL(app)

# 5. Define Routes (Updated for Database Interaction)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        # Create a cursor to execute queries
        cursor = mysql.connection.cursor()

        # Get user by username
        result = cursor.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            user = cursor.fetchone()
            stored_password_hash = user['password']

            # Compare passwords
            if check_password_hash(stored_password_hash, password_candidate):
                flash('Login successful!', 'success')
                # Here you would typically set up a session
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
        else:
            flash('Invalid username or password.', 'danger')

        cursor.close()
        return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Create cursor
        cursor = mysql.connection.cursor()
        
        try:
            # Execute query to insert new user
            cursor.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, hashed_password))
            
            # Commit to the database
            mysql.connection.commit()
            flash('Registration successful! You can now log in.', 'success')
        except Exception as e:
            # If the username is already taken (due to UNIQUE constraint)
            flash('Username already exists.', 'danger')
        finally:
            # Close connection
            cursor.close()

        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return "<h1>Welcome to the Dashboard!</h1><p>You are logged in with a database-backed account.</p>"

# Run the Application
if __name__ == '__main__':
    app.run(debug=True)
