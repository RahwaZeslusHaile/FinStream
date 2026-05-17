
from database import Base, engine
from sqlalchemy import Column, String, Float, Integer


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    quantity = Column(Float, index=True)
    broker = Column(String, index=True)
    market_value = Column(Float, index=True)

Base.metadata.create_all(bind=engine)    
