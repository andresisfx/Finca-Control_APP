"""
Modelo ProduccionVendedorDiaria — registro diario de litros entregados por un vendedor.
"""


from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ProduccionVendedorDiaria(Base):
    __tablename__ = "produccion_vendedor_diaria"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vendedor_id: Mapped[int] = mapped_column(
        ForeignKey("vendedores.id", ondelete="CASCADE"), nullable=False
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    litros: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # ── Relaciones ──
    vendedor: Mapped["Vendedor"] = relationship(
        "Vendedor", back_populates="producciones"
    )

    def __repr__(self) -> str:
        return (
            f"<ProduccionVendedorDiaria id={self.id} "
            f"fecha={self.fecha} litros={self.litros}>"
        )
