from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from models.models import RolUsuario, TipoEntrada, TipoPoder


# ---------- Usuarios ----------
class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol: RolUsuario = RolUsuario.lector


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ---------- Regiones ----------
class RegionBase(BaseModel):
    nombre: str
    slug: str
    descripcion: Optional[str] = None


class RegionCreate(RegionBase):
    pass


class RegionResponse(RegionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ---------- Zonas ----------
class ZonaBase(BaseModel):
    nombre: str
    slug: str
    descripcion: Optional[str] = None
    region_id: int
    zona_padre_id: Optional[int] = None


class ZonaCreate(ZonaBase):
    pass


class ZonaResponse(ZonaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ---------- Entradas de la wiki ----------
class EntradaWikiBase(BaseModel):
    tipo: TipoEntrada
    nombre: str
    slug: str
    descripcion: Optional[str] = None
    contenido: Optional[str] = None


class EntradaWikiCreate(EntradaWikiBase):
    creado_por: Optional[int] = None


class EntradaWikiResponse(EntradaWikiBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    creado_por: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# ---------- Detalle: Poder ----------
class PoderDetalleBase(BaseModel):
    tipo_poder: TipoPoder


class PoderDetalleResponse(PoderDetalleBase):
    model_config = ConfigDict(from_attributes=True)
    entrada_id: int
