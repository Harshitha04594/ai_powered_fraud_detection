from sqlalchemy import Column, Integer, String, Float
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    image_path = Column(String, nullable=False)
    date = Column(String, nullable=False)

class Return(Base):
    __tablename__ = "returns"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, nullable=False)
    return_image_path = Column(String, nullable=False)
    similarity_score = Column(Float, nullable=False)
    status = Column(String, default="Pending")
