from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import class_mapper

from Shared.Enums.models.db_tables import DBTable

class Base(DeclarativeBase):
    pass

class CountryDetail(Base):
    __tablename__ = "country_detail"

    id: Mapped[int] = mapped_column(primary_key=True)
    iso: Mapped[str] = mapped_column(String(50))
    country: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"CountryDetail(id={self.id!r}, iso={self.iso!r}, id={self.country!r})"
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in class_mapper(self.__class__).mapped_table.c}