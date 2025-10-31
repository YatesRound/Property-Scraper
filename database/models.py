from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Base class
Base = declarative_base()

# Property table
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(String)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    location = Column(String)
    image_url = Column(String)
    description = Column(Text, nullable=True)
    url = Column(String)

# SQLite setup
DATABASE_URL = "sqlite:///./properties.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Initialize database
def init_db():
    Base.metadata.create_all(engine)

# Fetch all properties
def get_all_properties():
    session = SessionLocal()
    data = session.query(Property).all()
    result = [vars(p) for p in data]
    for r in result:
        r.pop("_sa_instance_state", None)
    session.close()
    return result
