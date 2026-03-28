from backend.database import Base, engine
from backend.classes import Base

Base.metadata.create_all(bind=engine)