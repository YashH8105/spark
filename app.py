from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the root URL
@app.route('/')
def home():
    # Use render_template to return the HTML file
    return render_template('login.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
