from app.db.database import Base, engine
from app.models import File, FeatureMeasurement


def init_db():
    Base.metadata.create_all(bind=engine)