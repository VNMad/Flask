from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/users/<last_name>/<first_name>')
def username(first_name: str, last_name: str):
    return f'Hello, {last_name.upper()} {first_name[0].upper()}.'


if __name__ == '__main__':
    app.run(debug=True)

