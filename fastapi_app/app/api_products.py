from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .db import get_db
from .models import Product


router = APIRouter(prefix="/productos", tags=["productos"])


class ProductCreate(BaseModel):
    p_cat_id: int
    cat_id: int
    product_title: str
    product_price: int
    product_keywords: str = ""
    product_desc: str = ""
    product_img1: str = ""
    product_img2: str = ""


class ProductOut(ProductCreate):
    products_id: int

    class Config:
        orm_mode = True


@router.post("", response_model=ProductOut)
def create_product(body: ProductCreate, db: Session = Depends(get_db)) -> Product:
    """
    Crea un nuevo producto en el catálogo.
    """
    prod = Product(
        p_cat_id=body.p_cat_id,
        cat_id=body.cat_id,
        product_title=body.product_title,
        product_price=int(body.product_price),
        product_keywords=body.product_keywords,
        product_desc=body.product_desc,
        product_img1=body.product_img1,
        product_img2=body.product_img2,
    )
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod


@router.get("", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    """
    Devuelve todos los productos del catálogo.
    """
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    """
    Devuelve el detalle de un producto por ID.
    """
    prod = db.query(Product).filter(Product.products_id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod

