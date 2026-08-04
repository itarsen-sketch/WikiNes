from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.database import get_db
from models.models import EntradaWiki
from schemas.schemas import EntradaWikiResponse

router = APIRouter(prefix="/entradas", tags=["Entradas"])


@router.get("/", response_model=list[EntradaWikiResponse])
def buscar_entradas(
    q: Optional[str] = Query(None, description="Texto a buscar en nombre o descripción"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo, ej. 'personaje'"),
    db: Session = Depends(get_db),
):
    query = db.query(EntradaWiki)

    if q:
        busqueda = f"%{q}%"
        query = query.filter(
            or_(
                EntradaWiki.nombre.ilike(busqueda),
                EntradaWiki.descripcion.ilike(busqueda),
            )
        )

    if tipo:
        query = query.filter(EntradaWiki.tipo == tipo)

    return query.all()


@router.get("/{slug}", response_model=EntradaWikiResponse)
def obtener_entrada(slug: str, db: Session = Depends(get_db)):
    return db.query(EntradaWiki).filter(EntradaWiki.slug == slug).first()