from sqlalchemy import Column, Integer, Text, VARCHAR, TIMESTAMP, func
from app.db import Base

class RequestHistory(Base):
    __tablename__ = "requests_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_text = Column(Text, nullable=False)
    result_text = Column(Text, nullable=False)
    model_name = Column(VARCHAR(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())