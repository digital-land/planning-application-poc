import csv
import json
from datetime import datetime
from pathlib import Path

import requests
import shapely
from flask.cli import AppGroup
from sqlalchemy import and_, text

from application.models import Organisation, PlanningApplication, PlanningApplicationLog

data_cli = AppGroup("data")

datasette_orgs_query = """
https://datasette.planning.data.gov.uk/digital-land.json?_shape=objects&sql=select+entity%2C+organisation%2C+name%2C+website+%0D%0Afrom+organisation+where+entity+in+%28%3Ap0%2C+%3Ap1%2C+%3Ap2%2C+%3Ap3%29+order+by+organisation+limit+101&p0=382&p1=90&p2=26&p3=231"""  # noqa


@data_cli.command("load")
def load_data():
    from application.extensions import db

    resp = requests.get(datasette_orgs_query).json()

    for org in resp["rows"]:
        if Organisation.query.get(org["entity"]) is None:
            organisation = Organisation(**org)
            db.session.add(organisation)

    db.session.commit()

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
    from sqlalchemy.sql import text as sa_text

    from application.extensions import db

    db.session.execute(sa_text("TRUNCATE TABLE organisation CASCADE"))

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


@data_cli.command("geojson")
def make_geojson():
    from application.extensions import db

    db.session.execute(
        text("UPDATE planning_application SET geojson = NULL WHERE geojson = 'null';")
    )

    print("setting geojson if needed")
    batch_size = 5000
    batch = []
    for planning_application in PlanningApplication.query.filter(
        and_(
            PlanningApplication.geometry.is_not(None),
            PlanningApplication.geojson.is_(None),
        )
    ).all():
        wkt = shapely.from_wkt(planning_application.geometry)
        geojson = shapely.geometry.mapping(wkt)
        planning_application.geojson = geojson
        batch.append(planning_application)
        if len(batch) == batch_size:
            db.session.bulk_save_objects(batch)
            db.session.commit()
            print(f"saved {len(batch)} records")
            batch = []

    if len(batch) > 0:
        db.session.bulk_save_objects(batch)
        db.session.commit()
        print(f"saved last {len(batch)} records")

    print("done")
