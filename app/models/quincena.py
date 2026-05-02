"""
Modelo Quincena — período quincenal para agrupar producción y entregas.
"""



import uuid
from datetime import date
from sqlalchemy import Date, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Quincena(Base):
    __tablename__ = "quincenas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    finca_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("fincas.id", ondelete="CASCADE"), nullable=False
    )
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)

    # ── Relaciones ──
    finca: Mapped["Finca"] = relationship("Finca", back_populates="quincenas")
    precios: Mapped[list["PrecioLeche"]] = relationship(
        "PrecioLeche", back_populates="quincena", cascade="all, delete-orphan"
    )
    entregas: Mapped[list["Entrega"]] = relationship(
        "Entrega", back_populates="quincena", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Quincena id={self.id} {self.fecha_inicio} → {self.fecha_fin}>"
