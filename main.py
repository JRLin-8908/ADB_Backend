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

@app.route('/', methods = ['POST'])
def index():
    festival = 'xmassorder2011' if request.json['festival'] == 'Xmas' else 'chines_new_year'
    item = request.json['item']
    district = request.json['district']

    res = []
    if festival and item and district:

        if item == 'Suppliers':
            sql_cmd = """\
                SELECT s.latitude, s.longitude
                FROM public.supplier AS s
                JOIN public.county_moi_1090820 AS c
                ON ST_Intersects(s.geom, c.geom)

            """
            if district != '全臺灣': sql_cmd = sql_cmd + "WHERE c.countyname = {district}"

        else:
            sql_cmd = """\
                SELECT f.latitude, f.longitude
                FROM public.{festival} AS f
                JOIN public.county_moi_1090820 AS c
                ON ST_Intersects(f.geom, c.geom)

            """
            if district != '全臺灣': sql_cmd = sql_cmd + "WHERE c.countyname = {district}"

        query_data = db.engine.execute(sql_cmd)
        for row in query_data:
            res.append(dict(zip(['lat', 'lng'], row)))

    return json.dumps(res)


if __name__ == "__main__":
    app.run()