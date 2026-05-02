"""
Modelo Comprador — comprador de leche asociado a una finca.
"""


import uuid
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Comprador(Base):
    __tablename__ = "compradores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    finca_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("fincas.id", ondelete="CASCADE"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # ── Relaciones ──
    finca: Mapped["Finca"] = relationship("Finca", back_populates="compradores")
    entregas: Mapped[list["Entrega"]] = relationship(
        "Entrega", back_populates="comprador", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Comprador id={self.id} nombre={self.nombre!r}>"
