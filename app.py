from flask import Flask, request

# Initialize the Flask application
app = Flask(__name__)

# --- HTML Template stored as a Python multi-line f-string ---
# The {message} placeholder will be filled dynamically
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Simple Login</title>
    <!-- Link to the external CSS file -->
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <form action="/" method="post">
            <input type="text" id="username" name="username" placeholder="Username" required>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <input type="submit" value="Login">
        </form>
        <!-- Display messages here -->
        <p class="message">{message}</p>
    </div>
</body>
</html>
"""

# A simple, hardcoded user credential
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# Define a single route that handles both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
    # This message will be displayed on the login page
    message = ""

    # Check if the request method is POST (i.e., the form was submitted)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the submitted credentials are valid
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            # If valid, show a success message
            return "<h1>Login Successful!</h1><p>Welcome, admin.</p>"
        else:
            # If invalid, set an error message
            message = "Invalid username or password. Please try again."

    # For a GET request or a failed login, render the HTML template
    # The .format() method inserts the message into the {message} placeholder
    return HTML_TEMPLATE.format(message=message)

# Run the application
if __name__ == '__main__':
    # debug=True allows you to see errors and auto-reloads the server on changes
    app.run(debug=True)
