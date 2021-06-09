from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def fun():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


# heroku container:push web --app mypaysys
# sudo heroku container:release web --app mypaysys