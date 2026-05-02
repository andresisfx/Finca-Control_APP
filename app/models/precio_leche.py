"""
Modelo PrecioLeche — precios de compra y venta de leche por quincena.
"""


from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PrecioLeche(Base):
    __tablename__ = "precios_leche"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quincena_id: Mapped[int] = mapped_column(
        ForeignKey("quincenas.id", ondelete="CASCADE"), nullable=False
    )
    precio_compra: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    precio_venta: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    # ── Relaciones ──
    quincena: Mapped["Quincena"] = relationship(
        "Quincena", back_populates="precios"
    )

    def __repr__(self) -> str:
        return (
            f"<PrecioLeche id={self.id} "
            f"compra={self.precio_compra} venta={self.precio_venta}>"
        )
