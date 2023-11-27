# Import necessary modules from Flask
from flask import Flask, render_template, request

# Create an instance of the Flask class
app = Flask(__name__)

# Initialize an empty list to store collected data
collected_data = []

# Define a route for the root URL ('/')
@app.route('/')
def index():
    # When a user accesses the root URL, render the 'index.html' template
    # and pass the collected_data to the template
    return render_template('index.html', data=collected_data)

# Define a route for the '/collect_data' URL with the HTTP method 'POST'
@app.route('/collect_data', methods=['POST'])
def collect_data():
    # Retrieve the data submitted by the user from the HTML form
    user_data = request.form['user_data']
    
    # Append the user's data to the collected_data list
    collected_data.append(user_data)
    
    # After collecting the data, render the 'index.html' template
    # and pass the updated collected_data to the template
    return render_template('index.html', data=collected_data)

# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    # Start the Flask development server on '0.0.0.0' (accessible from any IP address)
    # and port 5000
    app.run(host='0.0.0.0', port=5000)
