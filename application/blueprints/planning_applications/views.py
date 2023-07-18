import datetime
import re

from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import and_

from application.models import Organisation, PlanningApplication, PlanningApplicationLog

planning_app = Blueprint(
    "planning_application", __name__, url_prefix="/planning-application"
)


status_map = {"live": "Live", "decision-made": "Decided"}


@planning_app.route("/")
def index():
    reference = request.args.get("planning_application_reference")

    if reference:
        return redirect(url_for("planning_application.plan", reference=reference))

    page_size = current_app.config.get("PAGE_SIZE", 50)
    page = request.args.get("page", 1, type=int)

    query = PlanningApplication.query

    if request.args.get("planning_authority"):
        ids = (
            Organisation.query.filter(
                Organisation.organisation.in_(
                    request.args.getlist("planning_authority")
                )
            )
            .with_entities(Organisation.entity)
            .all()
        )
        ids = [id[0] for id in ids]
        query = query.filter(PlanningApplication.organisation_entity.in_(ids))

    if request.args.get("decision") and request.args.get("decision") != "all":
        decision_status = request.args.get("decision")
        status = status_map.get(decision_status, None)
        if status is not None:
            query = query.filter(
                PlanningApplication.json["planning-application-status"].astext == status
            )

    if (
        request.args.get("entry_date_day")
        and request.args.get("entry_date_month")
        and request.args.get("entry_date_year")
    ):
        day = request.args.get("entry_date_day")
        month = request.args.get("entry_date_month")
        year = request.args.get("entry_date_year")
        date_str = f"{year}{month}{day}"
        date = datetime.datetime.strptime(date_str, "%Y%m%d")
        query = query.filter(
            and_(
                PlanningApplication.logs.any(PlanningApplicationLog.event_date >= date),
                PlanningApplication.logs.any(
                    PlanningApplicationLog.name == "submitted"
                ),
            )
        )

    planning_applications = query.paginate(
        page=page, per_page=page_size, error_out=False
    )

    # pass on filter args in pagination links
    args = request.args.copy()
    if "page" in args:
        del args["page"]

    if planning_applications.has_next:
        next_url = url_for(
            "planning_application.index", page=planning_applications.next_num, **args
        )
    else:
        next_url = None

    if planning_applications.has_prev:
        prev_url = url_for(
            "planning_application.index", page=planning_applications.prev_num, **args
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
    if re.search(r"^\s+|\s+$", reference):
        reference = reference.strip()
        return redirect(url_for("planning_application.plan", reference=reference))

    planning_application = PlanningApplication.query.get(reference)
    if planning_application is None:
        return abort(404)

    return render_template(
        "planning_application/application.html",
        planning_application=planning_application,
        properties=planning_application.json,
        logs=planning_application.logs,
    )
