from flask import Flask, render_template, request

app = Flask(__name__)

collected_data = []

@app.route('/')
def index():
    return render_template('index.html', data=collected_data)

@app.route('/collect_data', methods=['POST'])
def collect_data():
    user_data = request.form['user_data']
    collected_data.append(user_data)
    return render_template('index.html', data=collected_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
