import csv
import json
from datetime import datetime
from pathlib import Path

from flask.cli import AppGroup

from application.models import PlanningApplication, PlanningApplicationLog

data_cli = AppGroup("data")


@data_cli.command("load")
def load_data():
    from application.extensions import db

    planning_application_csv = (
        f"{Path(__file__).parent.parent}/data/planning-application.csv"
    )

    with open(planning_application_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            copy = _get_insert_copy(row)
            planning_application = PlanningApplication(**copy)
            db.session.add(planning_application)

    db.session.commit()

    planning_application_log_csv = (
        f"{Path(__file__).parent.parent}/data/planning-application-log.csv"
    )
    with open(planning_application_log_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            copy = _get_insert_copy(row)
            log = PlanningApplicationLog(**copy)
            try:
                db.session.add(log)
                db.session.commit()
            except Exception as e:
                print("error loading log with reference", log.reference, e)
                db.session.rollback()

    print("Planning Applications loaded")


@data_cli.command("drop")
def drop_data():
    from application.extensions import db

    PlanningApplicationLog.query.delete()
    PlanningApplication.query.delete()

    db.session.commit()

    print("Planning Applications dropped")


def _get_insert_copy(row):
    copy = row.copy()
    for key, val in copy.items():
        if val == "":
            val = None
            copy[key] = val
        if (key == "json" or key == "geojson") and val is not None:
            copy[key] = json.loads(val)
        if "date" in key and val is not None:
            copy[key] = datetime.strptime(val, "%Y-%m-%d").date()
        if (key == "entity" or key == "organisation_entity") and val is not None:
            copy[key] = int(val)
    return copy
