from   flask               import Flask, request, jsonify, make_response
from   flask_sqlalchemy    import SQLAlchemy
import time
import requests
import json
import secret

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']        = 'mysql+pymysql://' + secret.db_usr + ":" + secret.db_psk + "@" + secret.db_ip + '/RPS-DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class RPSPrice(db.Model):
    ID      = db.Column(db.String(50),primary_key=True)  # ID
    price   = db.Column(db.Float)                        # Price


    def __init__(self, ID, price):
        self.ID     = ID
        self.price    = price

db.create_all()

def precio_token(contrato):
    url = "https://api.pancakeswap.info/api/v2/tokens/" + contrato
    response = requests.get(url)
    return json.loads(response.text)

def prepare_number(num):
    out = str(num)
    if(len(out) != 2):
        out = "0" + out
    return out

def get_time_str():
    gmt = time.gmtime()
    return str(gmt.tm_year) + prepare_number(gmt.tm_mon) + prepare_number(gmt.tm_mday) + prepare_number(gmt.tm_hour) + prepare_number(gmt.tm_min)

lstString = get_time_str()

while(1):
    try:
        newString = get_time_str() #Resolution one minute
        if(lstString == newString):
            time.sleep(1)
            continue
        else:
            price = round(float(precio_token(secret.contract)['data']['price']), 4)
            lstString = newString
            new_post = RPSPrice(ID =lstString, price=price)
            db.session.add(new_post)
            db.session.commit()
            print(lstString , " ==> " , price)
    except:
        db.session.rollback()
        time.sleep(10)
        continue

