from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Text, String


class Exhibitor(SQLModel, table=True):
    __tablename__ = "exhibitor"

    id: int | None = Field(default=None, primary_key=True)
    exhib_name: str = Field(sa_column=Column(String(100)))
    img_url: str
    tel: str = Field(sa_column=Column(String(20)))
    adres: str = Field(sa_column=Column(String(100)))
    mail: str = Field(sa_column=Column(String(100)))
    site_url: str = Field(sa_column=Column(String(150)))
    description: str = Field(sa_column=Column(Text))
    category_id: int | None = Field(default=None, foreign_key="category.id")

    def __repr__(self):
        return f"<Exhibitor {self.exhib_name}>"