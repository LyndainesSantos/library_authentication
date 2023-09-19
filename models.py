from sqlalchemy import Column, Integer, String
from database import Base

class Livros(Base):
    __tablename__ = "livros"

    id: int = Column(Integer, primary_key=True, index=True)
    titulo: str = Column(String(100), nullable=False)
    descricao: str = Column(String(255), nullable=False)
    numero_paginas: int = Column(Integer, nullable=False)
