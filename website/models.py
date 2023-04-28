from datetime import datetime
from typing import List
from typing_extensions import Annotated
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

db = SQLAlchemy(add_models_to_shell=True)

intpk = Annotated[int, mapped_column(primary_key=True)]
str_username = Annotated[str, mapped_column(String(30))]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(String(50))
    username: Mapped[str_username] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(100))
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User: {self.email}>"


class Reservation(Base):
    __tablename__ = "reservation"
    id: Mapped[intpk]
    time: Mapped[datetime]
    user_username: Mapped[str_username] = mapped_column(ForeignKey("user.username"))
    user: Mapped["User"] = relationship(back_populates="reservations")

    def __repr__(self):
        return f"<Reservation: {self.time}>"
