from flask import Blueprint, abort, render_template

from application.models import PlanningApplication

planning_app = Blueprint(
    "planning_application", __name__, url_prefix="/planning-application"
)


@planning_app.route("/")
def index():
    planning_applications = PlanningApplication.query.all()
    return render_template(
        "planning_application/index.html", planning_applications=planning_applications
    )


@planning_app.route("/<path:reference>")
def plan(reference):
    planning_application = PlanningApplication.query.get(reference)
    if planning_application is None:
        return abort(404)

    return render_template(
        "planning_application/application.html",
        planning_application=planning_application,
        properties=planning_application.json,
        logs=planning_application.logs,
    )
