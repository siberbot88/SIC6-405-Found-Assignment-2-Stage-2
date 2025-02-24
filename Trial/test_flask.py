from flask import Flask

app = Flask(__name__)

@app.route('/')
def entry_point():
    return 'Hello world'

if __name__ == '__name__':
    app.run(debug=True)