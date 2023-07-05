from flask import Blueprint, render_template

planning_app = Blueprint(
    "planning_application", __name__, url_prefix="/planning-application"
)


@planning_app.route("/")
def index():
    planning_applications = {}
    return render_template(
        "planning_application/index.html", planning_applications=planning_applications
    )


@planning_app.route("/<string:reference>")
def plan(reference):
    planning_application = {"reference": reference}

    return render_template(
        "planning_application/application.html",
        planning_application=planning_application,
    )
