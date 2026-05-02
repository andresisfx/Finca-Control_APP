"""
Modelo Evento — eventos asociados a un animal (salud, reproducción, etc.).
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Text, func, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# 🔹 ENUM de tipos de evento
class TipoEvento(str, Enum):
    VACUNACION = "vacunacion"
    ENFERMEDAD = "enfermedad"
    PARTO = "parto"
    CELO = "celo"
    MONTA = "monta"
    SERVICIO = "servicio"
    VENDIDO = "vendido"
    MUERTE = "muerte"
    


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    animal_id: Mapped[int] = mapped_column(
        ForeignKey("animales.id", ondelete="CASCADE"),
        nullable=False
    )

    
    tipo: Mapped[TipoEvento] = mapped_column(
        SQLEnum(TipoEvento, name="tipo_evento_enum"),
        nullable=False
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    nota: Mapped[str | None] = mapped_column(Text, nullable=True)

    metadata_extra: Mapped[dict | None] = mapped_column(
        "metadata",
        JSON,
        nullable=True
    )

    # ── Relaciones ──
    animal: Mapped["Animal"] = relationship(
        "Animal",
        back_populates="eventos"
    )

    def __repr__(self) -> str:
        return f"<Evento id={self.id} tipo={self.tipo.value!r} animal_id={self.animal_id}>"