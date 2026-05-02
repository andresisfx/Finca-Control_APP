"""
Modelo Finca — representa una finca perteneciente a un usuario.
"""


import uuid
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Finca(Base):
    __tablename__ = "fincas"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # ── Relaciones ──
    usuario: Mapped["User"] = relationship("User", back_populates="fincas")
    animales: Mapped[list["Animal"]] = relationship(
        "Animal", back_populates="finca", cascade="all, delete-orphan"
    )
    vendedores: Mapped[list["Vendedor"]] = relationship(
        "Vendedor", back_populates="finca", cascade="all, delete-orphan"
    )
    compradores: Mapped[list["Comprador"]] = relationship(
        "Comprador", back_populates="finca", cascade="all, delete-orphan"
    )
    quincenas: Mapped[list["Quincena"]] = relationship(
        "Quincena", back_populates="finca", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Finca id={self.id} nombre={self.nombre!r}>"
