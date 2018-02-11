from sanic import Sanic
from endpoint import bp_db

app = Sanic(__name__)
app.blueprint(bp_db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', workers=2, port=10010, debug=True)