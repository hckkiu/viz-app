from flask import Blueprint, request, session, render_template, send_file
from . import db
from .models import Data
from .plots import *
from .utils import *
import pandas as pd
from io import BytesIO
from requests.utils import unquote
import os
import json


CHARTS_CONFIG = json.load(open(os.path.join(os.path.dirname(__name__), "app/config/charts_config.json")))
CHARTS = list(CHARTS_CONFIG.keys())



routes = Blueprint("routes", __name__)

@routes.route("/upload-data", methods=["POST"])
def upload_data():

    res = request.files.get("files")
    df = pd.read_csv(BytesIO(res.read()))

    data = Data(data=df.to_csv(index=False))
    db.session.add(data)
    db.session.commit()

    session["ids"] = session.get("ids", []) + [data.id]

    return {}


@routes.route("/get-data", methods=["POST"])
def get_data():
    df = get_data_to_df()
    return df.to_dict(orient="records")


@routes.route("/create-config-html", methods=["POST"])
def create_config_html():
    
    selected_chart = request.values.get("chart")
    selected_chart = CHARTS[0] if selected_chart is None else selected_chart
    num = request.values.get("n")
    num = 1 if num is None else num

    charts = [
        {"chart": chart, "selected": "selected"} if chart == selected_chart else {"chart": chart, "selected": ""}
        for chart in CHARTS
    ]
    data_input_config = CHARTS_CONFIG[selected_chart]["data_input"]

    df = get_data_to_df()
    columns = df.columns.to_list()
    cat_columns = df.select_dtypes(include=["object"]).columns.to_list()
    num_columns = df.select_dtypes(include=["number"]).columns.to_list()

    data_input = []
    for config in data_input_config:
    
        if config["type"] == "number":
            config["columns"] = num_columns
        elif config["type"] == "number+empty":
            config["columns"] = [""] + num_columns
        elif config["type"] == "category":
            config["columns"] = cat_columns
        elif config["type"] == "category+empty":
            config["columns"] = [""] + cat_columns
        elif config["type"] == "both":
            config["columns"] = columns
        elif config["type"] == "both+empty":
            config["columns"] = [""] + columns
        else:
            config["columns"] = [""] + columns
        data_input.append(config)
    
    html = render_template("create_config.html", num=num, charts=charts, data_input=data_input)
    return {"html": html}


@routes.route("/create-chart-html", methods=["POST"])
def create_chart_html():
    res = request.form
    df = get_data_to_df()
    input = make_input(res, df)
    html = create_plot_html(**input)
    return html


@routes.route("/generate-all", methods=["POST"])
def generate_all():

    res = request.values.getlist("data[]")
    print(1, request.values)
    print(2, request.data)
    print(3, request.form)
    heading = request.values.get("heading")
    comment = request.values.get("comment")

    df = get_data_to_df()
    inputs = []
    for input_str in res:
        input_lst = input_str.split("&")
        input_lst = [i.split("=") for i in input_lst]
        data = {i[0]: unquote(i[-1]) for i in input_lst}
        input = make_input(data, df)
        inputs.append(input)

    html = create_all(inputs)
    html = render_template("output.html", content=html, heading=heading, comment=comment)
    bio = BytesIO()
    bio.write(html.encode('utf-8'))
    bio.seek(0)
    return send_file(bio, mimetype="text/html")


@routes.route("/remove-prev-ids", methods=["POST"])
def remove_prev_ids():
    ids = session.get("ids")
    try:
        if ids is not None:
            ids = ids[:-1]
            sql = Data.__table__.delete().where(Data.id.in_(ids))
            db.session.execute(sql)
            db.session.commit()
            ids = ids[-1]
    except:
        pass
    return {}
