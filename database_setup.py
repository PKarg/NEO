from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float

SQLALCHEMY_DATABASE_URL = "sqlite:///./neos.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class NEO(Base):
    __tablename__ = "neo"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String, unique=True, index=True)
    Epoch_MJD = Column(Float)
    SemMajAxis_AU = Column(Float)
    Ecc = Column(Float)
    Incl_deg = Column(Float)
    LongAscNode_deg = Column(Float)
    ArgP_deg = Column(Float)
    Mean_Anom_deg = Column(Float)
    AbsMag = Column(Float)
    SlopeParamG = Column(Float)
    Aphel_AU = Column(Float)
    Perihel_AU = Column(Float)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
