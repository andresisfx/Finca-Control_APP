"""
Modelo Entrega — registro de entregas de leche a un comprador en una quincena.
"""



from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Entrega(Base):
    __tablename__ = "entregas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    comprador_id: Mapped[int] = mapped_column(
        ForeignKey("compradores.id", ondelete="CASCADE"), nullable=False
    )
    quincena_id: Mapped[int] = mapped_column(
        ForeignKey("quincenas.id", ondelete="CASCADE"), nullable=False
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    litros: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # ── Relaciones ──
    comprador: Mapped["Comprador"] = relationship(
        "Comprador", back_populates="entregas"
    )
    quincena: Mapped["Quincena"] = relationship(
        "Quincena", back_populates="entregas"
    )

    def __repr__(self) -> str:
        return (
            f"<Entrega id={self.id} "
            f"fecha={self.fecha} litros={self.litros}>"
        )
