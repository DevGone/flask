from flask import Flask
from raspberric import getData
app = Flask(__name__)

@app.route("/")
def root():
    return getData()

if __name__ == "__main__":
    app.run()
