#"Symbol","Name","LastSale","MarketCap","IPOyear","Sector","industry","Summary Quote",
import csv, sqlite3

def parse_money_string(money):
    if money == 'n/a': return 0
    if money[0] == '$': money = money[1:]
    f = float(money[:-1])
    if money[-1] == 'M':
        f *= 1000000.0
    elif money[-1] == 'B':
        f *= 1000000000.0
    else:
        f = float(money)
    return f
    
def sanitize_stock(sdata):
    return (sdata[0], sdata[1], sdata[2], parse_money_string(sdata[3]), sdata[4], sdata[5], sdata[6], sdata[7])

db = sqlite3.connect('companies.db')
c = db.cursor()
c.execute('DROP TABLE stocks')
c.execute('''CREATE TABLE stocks (
symbol text,
name text,
lastsale numeric,
marketcap numeric,
ipoyear numeric,
sector text,
industry text, 
summary_quote text)
''')
with open('companies.csv', 'r') as companies:
    reader = csv.reader(companies)
    for row in reader:
        if row[0] == 'Symbol': continue
        sanitized = sanitize_stock(row)
        if sanitized[3] > 0:
            c.execute('INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?, ?)', sanitized)
    db.commit()
    db.close()


