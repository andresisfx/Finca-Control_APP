"""
Modelo Animal — representa ganado perteneciente a una finca.
"""


import uuid
from sqlalchemy import ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Animal(Base):
    __tablename__ = "animales"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    finca_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("fincas.id", ondelete="CASCADE"), nullable=False
    )
    codigo: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    nombre: Mapped[str | None] = mapped_column(String(150), nullable=True)
    foto_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relaciones ──
    finca: Mapped["Finca"] = relationship("Finca", back_populates="animales")
    eventos: Mapped[list["Evento"]] = relationship(
        "Evento", back_populates="animal", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Animal id={self.id} codigo={self.codigo!r}>"
