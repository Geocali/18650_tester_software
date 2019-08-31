from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def main():
    #return render_template('battery_test.html')

    img = 'static/battery/Batteries-1379208.svg'
    return render_template('battery_test.html', img=img)


if __name__ == "__main__":
    app.run()
