"""
Modelo Vendedor — proveedor de leche asociado a una finca.
"""


import uuid
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Vendedor(Base):
    __tablename__ = "vendedores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    finca_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("fincas.id", ondelete="CASCADE"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # ── Relaciones ──
    finca: Mapped["Finca"] = relationship("Finca", back_populates="vendedores")
    producciones: Mapped[list["ProduccionVendedorDiaria"]] = relationship(
        "ProduccionVendedorDiaria",
        back_populates="vendedor",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Vendedor id={self.id} nombre={self.nombre!r}>"
