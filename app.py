from flask_api import FlaskAPI
app = flask(__name__)

@app.route('/')
def hello():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True)