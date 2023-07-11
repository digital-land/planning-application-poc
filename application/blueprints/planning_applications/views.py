import json
import sqlite3

from flask import Blueprint, render_template

planning_app = Blueprint(
    "planning_application", __name__, url_prefix="/planning-application"
)


def db_connection():
    connection = sqlite3.connect("data/planning-application.sqlite3")
    connection.row_factory = sqlite3.Row
    return connection


@planning_app.route("/")
def index():
    connection = db_connection()
    planning_applications = connection.execute("SELECT * FROM entity").fetchall()
    connection.close()
    return render_template(
        "planning_application/index.html", planning_applications=planning_applications
    )


@planning_app.route("/<path:reference>")
def plan(reference):
    connection = db_connection()
    planning_application = connection.execute(
        "SELECT * FROM entity WHERE reference = ?", (reference,)
    ).fetchone()
    logs = connection.execute(
        "SELECT * FROM planning_application_log WHERE reference = ?", (reference,)
    ).fetchall()
    connection.close()
    props = planning_application["json"]
    properties = json.loads(props)

    return render_template(
        "planning_application/application.html",
        planning_application=planning_application,
        properties=properties,
        logs=logs,
    )
