from flask import Blueprint, abort, current_app, render_template, request, url_for

from application.models import PlanningApplication

planning_app = Blueprint(
    "planning_application", __name__, url_prefix="/planning-application"
)


@planning_app.route("/")
def index():
    page_size = current_app.config.get("PAGE_SIZE", 50)
    page = request.args.get("page", 1, type=int)
    planning_applications = PlanningApplication.query.paginate(
        page=page, per_page=page_size, error_out=False
    )

    if planning_applications.has_next:
        next_url = url_for(
            "planning_application.index", page=planning_applications.next_num
        )
    else:
        next_url = None

    if planning_applications.has_prev:
        prev_url = url_for(
            "planning_application.index", page=planning_applications.prev_num
        )
    else:
        prev_url = None

    return render_template(
        "planning_application/index.html",
        planning_applications=planning_applications,
        prev_url=prev_url,
        next_url=next_url,
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
