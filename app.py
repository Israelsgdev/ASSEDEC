from flask import Flask, render_template, request, flash

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    return render_template('/membros/dashboard.html')



if __name__ == '__main__':
    app.run(debug=True)