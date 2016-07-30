import sqlite3, random, flask

db = sqlite3.connect('companies.db', check_same_thread=False)
c = db.cursor()
c.execute("select count(*) from stocks")
numstocks = c.fetchone()[0]

def money_string(num):
    if num > 1000000000:
        return '$%dB' % (num / 1000000000)
    elif num > 1000000:
        return '$%dM' % (num / 1000000)
    else:
        return '$%d' % num

def get_random_stock():
    randrowid = random.randint(1, numstocks)
    c.execute('select * from stocks where rowid=?', (randrowid,))
    rando = c.fetchone()
    return {'symbol': rando[0],
            'name': rando[1],
            'price': rando[2],
            'marketcap': money_string(rando[3]),
            'ipoyear': rando[4],
            'sector': rando[5],
            'industry': rando[6],
            'url': rando[7]}

app = flask.Flask(__name__)

@app.route('/random.json')
def get_random_json():
    return flask.jsonify(**get_random_stock())

@app.route('/')
def index():
    return flask.render_template('index.html', **get_random_stock())

if __name__=="__main__":
    app.run(debug=True)
