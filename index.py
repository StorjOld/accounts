import flask
import accounts
import settings

app = flask.Flask(__name__)

def accounts():
    a = getattr(flask.g, '_accounts', None)
    if a is None:
        a = flask.g._accounts = accounts.Manager(settings.DATABASE_PATH)

    return a

def authenticate(f):
    def f2(*args, **kwargs):
        api_key = request.headers.get('Authentication', None)

        if not accounts().valid_api_key(api_key):
            return flask.jsonify(status="invalid-authentication"), 401
        else:
            return f(*args, **kwargs)

    f2.__name__ = f.__name__
    return f2


@app.route("/accounts/token/new", methods=['POST'])
def token_new():
    tm = accounts()

    return flask.jsonify(token=tm.generate())


@app.route("/accounts/token/prices", methods=['GET'])
def token_prices():
    tm = accounts()

    return flask.jsonify(prices=[
        {
            "amount": price.amount,
            "cost": price.cost
        }
        for price in tm.prices()])


@app.route("/accounts/token/balance/<token>", methods=['GET'])
def token_balance(token):
    tm = accounts()

    return flask.jsonify(balance=tm.balance(token))


@app.route("/accounts/token/redeem/<token>", methods=['POST'])
def token_redeem(token):
    tm = accounts()

    promocode = None if request.json is None else request.json.get('promocode', None)

    if promocode and tm.redeem(token, promocode):
        return flask.jsonify(status="ok"), 201
    else:
        return flask.jsonify(status="error"), 403


@app.route("/accounts/token/deposit/<token>", methods=['POST'])
@authenticate
def token_deposit(token):
    try:
        byte_amount = int(request.json.get('bytes', None))
    except:
        return flask.jsonify(status="bad-request"), 400

    tm.add(token, byte_amount)

    return flask.jsonify(status="ok")


@app.route("/accounts/token/withdraw/<token>", methods=['POST'])
@authenticate
def token_withdraw(token):
    tm = accounts()

    try:
        byte_amount = int(request.json.get('bytes', None))
    except:
        return flask.jsonify(status="bad-request"), 400

    if tm.consume(token, byte_amount):
        return flask.jsonify(status="ok"), 200
    else:
        return flask.jsonify(error='balance-insufficient'), 402


@app.route("/accounts/coinbase/success/<api_key>/<int:bytes>", methods=['POST'])
def coinbase_success(api_key, bytes):
    tm = accounts()

    if not tm.api_key.valid_api_key(api_key):
        return flask.jsonify(status="invalid-authentication"), 401

    # Return a bad request if custom param is missing
    try:
        data = request.json.get('order', None)
        token = data['custom']
    except:
        return flask.jsonify(status="bad-request"), 400

    tm.add(token, bytes)

    return flask.jsonify(status="ok"), 200
