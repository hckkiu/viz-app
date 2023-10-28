from flask import session
from .models import Data
import pandas as pd
from io import StringIO
from .plots import *

def get_data_to_df():
    ids = session.get("ids")
    id = ids[-1]
    res = Data.query.filter_by(id=id).first()
    df = pd.read_csv(StringIO(res.data))
    return df

def make_input(data, df):
    chart = data.get("chart")
    x = data.get("x")
    y = data.get("y")
    z = data.get("z")
    color = data.get("color")
    line_group = data.get("line group")
    xlabel = data.get("x-label")
    ylabel = data.get("y-label")
    title = data.get("title")
    sort = data.get("sort")

    color = None if color == "" else color

    if sort is not None and sort != "":
        df = df.sort_values(sort)
    
    if chart == "Bar":
        df = df.groupby(x).size().reset_index()
        y = 0
    
    if chart == "Line":
        if color is not None and color != "":
            df = df[[x, y, color]].groupby([x, color]).sum().reset_index()
        else:
            df = df[[x, y]].groupby(x).sum().reset_index()
        print(df)

    if chart == "Area":
        print(111, line_group)
        if color is not None and color != "" and line_group is not None and line_group != "":
            print(1)
            df = df[[x, y, line_group, color]].groupby([x, line_group, color]).sum().reset_index()
        elif color is not None and color != "":
            print(2)
            df = df[[x, y, color]].groupby([x, color]).sum().reset_index()
        else:
            print(3)
            df = df[[x, y]].groupby(x).sum().reset_index()
        print(df)
    
    if xlabel is None or xlabel == "":
        xlabel = x if x is not None and x != "" else ""
    if ylabel is None or ylabel == "":
        ylabel = y if y is not None and y != "" and y != 0 else ""

    if title is None or title == "":
        title = chart.upper()
    if xlabel is not None and xlabel != "":
        title += f" - {xlabel}"
    if ylabel is not None and ylabel != "":
        title += f" - {ylabel}"
    if color is not None and color != "":
        title += f" - {color}"
    
    input = {
        "chart": chart, 
        "data_frame": df, 
        "x": x, 
        "y": y, 
        "labels": {"x": xlabel, "y": ylabel}, 
        "color": color, 
        "title": title
    }

    if chart == "Scatter 3d":
        input["z"] = z

    if chart == "Area" and line_group is not None and line_group != "":
        input["line_group"] = line_group

    return input