import enum
from sqlalchemy import (
    Column, BigInteger, Text, TIMESTAMP, ForeignKey, Enum, Integer, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base


# ---------- Usuarios ----------
class RolUsuario(str, enum.Enum):
    lector = "lector"
    colaborador = "colaborador"
    moderador = "moderador"
    creador = "creador"
    admin = "admin"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True)
    nombre = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    rol = Column(Enum(RolUsuario, name="rol_usuario"), nullable=False, default=RolUsuario.lector)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


# ---------- Regiones y Zonas ----------
class Region(Base):
    __tablename__ = "regiones"

    id = Column(BigInteger, primary_key=True)
    nombre = Column(Text, nullable=False, unique=True)
    slug = Column(Text, nullable=False, unique=True)
    descripcion = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    zonas = relationship("Zona", back_populates="region")


class Zona(Base):
    __tablename__ = "zonas"

    id = Column(BigInteger, primary_key=True)
    nombre = Column(Text, nullable=False)
    slug = Column(Text, nullable=False, unique=True)
    descripcion = Column(Text)
    region_id = Column(BigInteger, ForeignKey("regiones.id", ondelete="CASCADE"), nullable=False)
    zona_padre_id = Column(BigInteger, ForeignKey("zonas.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    region = relationship("Region", back_populates="zonas")
    subzonas = relationship("Zona")


# ---------- Entradas de la wiki (tabla base) ----------
class TipoEntrada(str, enum.Enum):
    objeto = "objeto"
    animal = "animal"
    flora = "flora"
    estructura = "estructura"
    cultura = "cultura"
    religion = "religion"
    poder = "poder"
    personaje = "personaje"
    ciudad = "ciudad"
    evento_historico = "evento_historico"
    capitulo = "capitulo"
    historia = "historia"


class EntradaWiki(Base):
    __tablename__ = "entradas_wiki"

    id = Column(BigInteger, primary_key=True)
    tipo = Column(Enum(TipoEntrada, name="tipo_entrada"), nullable=False)
    nombre = Column(Text, nullable=False)
    slug = Column(Text, nullable=False, unique=True)
    descripcion = Column(Text)
    contenido = Column(Text)
    creado_por = Column(BigInteger, ForeignKey("usuarios.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


# ---------- Ubicaciones (M:N con region/zona) ----------
class EntradaUbicacion(Base):
    __tablename__ = "entrada_ubicaciones"

    id = Column(BigInteger, primary_key=True)
    entrada_id = Column(BigInteger, ForeignKey("entradas_wiki.id", ondelete="CASCADE"), nullable=False)
    region_id = Column(BigInteger, ForeignKey("regiones.id", ondelete="CASCADE"), nullable=False)
    zona_id = Column(BigInteger, ForeignKey("zonas.id", ondelete="SET NULL"))

    __table_args__ = (UniqueConstraint("entrada_id", "region_id", "zona_id"),)


# ---------- Relaciones genéricas entre entradas ----------
class EntradaRelacion(Base):
    __tablename__ = "entrada_relaciones"

    id = Column(BigInteger, primary_key=True)
    entrada_id = Column(BigInteger, ForeignKey("entradas_wiki.id", ondelete="CASCADE"), nullable=False)
    relacionada_id = Column(BigInteger, ForeignKey("entradas_wiki.id", ondelete="CASCADE"), nullable=False)
    tipo_relacion = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("entrada_id", "relacionada_id", "tipo_relacion"),
        CheckConstraint("entrada_id <> relacionada_id"),
    )


# ---------- Detalle: Poder ----------
class TipoPoder(str, enum.Enum):
    magico = "magico"
    fisico = "fisico"


class PoderDetalle(Base):
    __tablename__ = "poderes_detalle"

    entrada_id = Column(BigInteger, ForeignKey("entradas_wiki.id", ondelete="CASCADE"), primary_key=True)
    tipo_poder = Column(Enum(TipoPoder, name="tipo_poder"), nullable=False)


# ---------- Detalle: Capítulos ----------
class CapituloDetalle(Base):
    __tablename__ = "capitulos_detalle"

    entrada_id = Column(BigInteger, ForeignKey("entradas_wiki.id", ondelete="CASCADE"), primary_key=True)
    historia_id = Column(BigInteger, ForeignKey("entradas_wiki.id", ondelete="CASCADE"), nullable=False)
    numero_capitulo = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("historia_id", "numero_capitulo"),)

