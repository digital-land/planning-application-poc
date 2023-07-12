import uuid

from sqlalchemy.dialects.postgresql import JSONB, UUID

from application.extensions import db


def _generate_uuid():
    return uuid.uuid4()


class DateModel(db.Model):
    __abstract__ = True

    entry_date = db.Column(db.Date, default=db.func.current_date())
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def as_dict(self):
        return {
            "entry-date": self.entry_date,
            "start-date": self.start_date,
            "end-date": self.end_date,
        }


class PlanningApplication(DateModel):
    __tablename__ = "planning_application"

    reference = db.Column(db.String, primary_key=True)
    entity = db.Column(db.BigInteger)
    dataset = db.Column(db.String)
    geojson = db.Column(JSONB)
    geometry = db.Column(db.String)
    json = db.Column(JSONB)
    name = db.Column(db.String)
    organisation_entity = db.Column(db.BigInteger)
    point = db.Column(db.String)
    prefix = db.Column(db.String)
    typology = db.Column(db.String)
    logs = db.relationship(
        "PlanningApplicationLog", back_populates="planning_application"
    )


class PlanningApplicationLog(DateModel):
    __tablename__ = "planning_application_log"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=_generate_uuid)
    name = db.Column(db.String)
    event_date = db.Column(db.Date)
    reference = db.Column(db.String, db.ForeignKey("planning_application.reference"))
    planning_application = db.relationship("PlanningApplication", back_populates="logs")


# class PlanningApplicationDocument(DateModel):
#     __tablename__ = "planning_application_document"
#     pass
