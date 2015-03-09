from flask import Flask, render_template
from raspberric import getData
app = Flask(__name__)

@app.route("/")
def root():
    return "Yo bitch !"

@app.route("/getdata/")
@app.route("/getdata/<name>")
def test(name=None):
    return render_template('hello.html', name=name, data=getData())

if __name__ == "__main__":
    app.run()
