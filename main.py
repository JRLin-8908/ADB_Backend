import os
import json
import simplejson
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_cors import CORS

db = SQLAlchemy()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost/adb_final"

db.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    res = []
    #if request.is_json: print(request.json()['queryparam']['item'])
    #if request.method == 'GET': return json.dumps(res)
    param = request.get_json().get('queryparam', None)
    print('festival:')
    print(param.get('festival'))
    print('formfestival:')
    print(param.get('formfestival'))
    print('item:')
    print(param.get('item'))
    print('district:')
    print(param.get('district'))
    festival = 'chines_new_year' if param.get('formfestival', None) == 'CNY' else 'xmassorder2011'
    item = param.get('item', None)
    district = param.get('district', None)
    # print("*: " + festival)
    # print(item)
    # print(district)
    # print(simplejson.dumps([{"lat":123, "lng":456}]))
    # print(json.dumps([{"lat":123, "lng":456}]))

    if item == 'Suppliers':
        sql_cmd = """
            SELECT s.latitude, s.longitude
            FROM public.supplier AS s
            JOIN public.county_moi_1090820 AS c
            ON ST_Intersects(ST_Transform(s.geom, 4326), ST_Transform(c.geom, 4326))

        """
        if district != '全臺灣': sql_cmd = sql_cmd + f"WHERE c.countyname = \'{district}\'"

    else:
        sql_cmd = f"""
            SELECT f.latitude, f.longitude
            FROM public.{festival} AS f
            JOIN public.county_moi_1090820 AS c
            ON ST_Intersects(ST_Transform(f.geom, 4326), ST_Transform(c.geom, 4326))

        """
        if district != '全臺灣': sql_cmd = sql_cmd + f"WHERE c.countyname = \'{district}\'"

    print(sql_cmd)
    query_data = db.engine.execute(sql_cmd)
    print("yo~")
    for row in query_data:
        res.append(dict(zip(['lat', 'lng'], row)))
    k = simplejson.dumps(res, use_decimal=True)
    print(k)
    return k
    #return json.dumps([{"lat":123, "lng":456}])


if __name__ == "__main__":
    app.run(debug = True)