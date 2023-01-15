import os
import json
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost/adb_final"

db.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    res = []
    #if request.method == 'GET': return json.dumps(res)
    param = json.loads(request.get_data())['queryparam']
    festival = 'xmassorder2011' if param['festival'] == 'Xmas' else 'chines_new_year'
    item = param['item']
    district = param['district']

    if item == 'Suppliers':
        sql_cmd = """
            SELECT s.latitude, s.longitude
            FROM public.supplier AS s
            JOIN public.county_moi_1090820 AS c
            ON ST_Intersects(ST_Transform(s.geom, 4326), ST_Transform(c.geom, 4326))

        """
        if district != '全臺灣': sql_cmd = sql_cmd + "WHERE c.countyname = \'{district}\'"

    else:
        sql_cmd = """
            SELECT f.latitude, f.longitude
            FROM public.{festival} AS f
            JOIN public.county_moi_1090820 AS c
            ON ST_Intersects(ST_Transform(f.geom, 4326), ST_Transform(c.geom, 4326))

        """
        if district != '全臺灣': sql_cmd = sql_cmd + "WHERE c.countyname = \'{district}\'"

    query_data = db.engine.execute(sql_cmd)
    for row in query_data:
        res.append(dict(zip(['lat', 'lng'], row)))

    return json.dumps(res)
    #return json.dumps({"lat":123, "lng":456})


if __name__ == "__main__":
    app.run(debug = True)