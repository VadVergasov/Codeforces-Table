# -*- coding: utf-8  -*-
# Main program  Copyright (C) 2021  Vadim Vergasov
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.
import json
import math
import time

import flask
from codeforces_api import CodeforcesApi

app = flask.Flask(__name__)

STANDINGS = dict()
USERS = list()
USER_COUNTRY = dict()


@app.route("/get_countries", methods=["POST"])
def get_countries():
    api = CodeforcesApi()
    countries = set()
    for i in range(1, int(math.ceil(len(USERS) / 5000)) + 1):
        for user in api.user_info(USERS[(i - 1) * 5000 : min(i * 5000, len(USERS))])[
            "result"
        ]:
            try:
                USER_COUNTRY[user["handle"]] = user["country"]
                countries.add(user["country"])
            except KeyError:
                USER_COUNTRY[user["handle"]] = "None"
                countries.add("None")
        time.sleep(0.1)
    countries = list(countries)
    countries.sort()
    countries = tuple(countries)
    return json.dumps(countries)


@app.route("/set_contest", methods=["POST"])
def get_contest_countries():
    global STANDINGS, USERS
    api = CodeforcesApi()
    STANDINGS = api.contest_standings(flask.request.form["contest"])["result"]
    for i in STANDINGS["rows"]:
        USERS.append(i["party"]["members"][0]["handle"])
    return "OK"


@app.route("/get_standings", methods=["POST"])
def get_table():
    country = flask.request.form["country"]
    result = list()
    place = 1
    for row in STANDINGS["rows"]:
        if USER_COUNTRY[row["party"]["members"][0]["handle"]] == country:
            result.append(
                {
                    "handle": row["party"]["members"][0]["handle"],
                    "place": str(place),
                }
            )
        place += 1
    return json.dumps(result)


@app.route("/")
def index():
    return flask.render_template("index.html")


app.run()
