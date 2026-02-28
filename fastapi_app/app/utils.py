from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import Request
from sqlalchemy.orm import Session

from .models import Category, ProductCategory, CartItem, Product, Customer


REPO_ROOT = Path(__file__).resolve().parents[2]


def ensure_session_customer_email(request: Request) -> str:
    if "customer_email" not in request.session:
        request.session["customer_email"] = "unset"
    return request.session["customer_email"]


def is_logged_in(customer_email: str) -> bool:
    return bool(customer_email and customer_email != "unset")


def set_flash(request: Request, message: str) -> None:
    request.session["_flash"] = message


def pop_flash(request: Request) -> str | None:
    msg = request.session.get("_flash")
    if msg:
        request.session.pop("_flash", None)
    return msg


@dataclass(frozen=True)
class CartTotals:
    items_count: int
    total_price: int


def get_cart_totals(db: Session, customer_email: str) -> CartTotals:
    if not is_logged_in(customer_email):
        return CartTotals(items_count=0, total_price=0)

    items = db.query(CartItem).filter(CartItem.c_id == customer_email).all()
    items_count = len(items)
    total = 0
    if not items:
        return CartTotals(items_count=0, total_price=0)

    product_ids = [i.products_id for i in items]
    products = db.query(Product).filter(Product.products_id.in_(product_ids)).all()
    price_by_id = {p.products_id: int(p.product_price) for p in products}
    for i in items:
        total += int(price_by_id.get(i.products_id, 0)) * int(i.qty)
    return CartTotals(items_count=items_count, total_price=total)


def get_cart_preview_items(db: Session, customer_email: str, limit: int = 2) -> list[dict[str, Any]]:
    if not is_logged_in(customer_email):
        return []

    items = (
        db.query(CartItem)
        .filter(CartItem.c_id == customer_email)
        .order_by(CartItem.date.desc())
        .limit(limit)
        .all()
    )
    if not items:
        return []

    product_ids = [i.products_id for i in items]
    products = db.query(Product).filter(Product.products_id.in_(product_ids)).all()
    product_by_id = {p.products_id: p for p in products}

    out: list[dict[str, Any]] = []
    for i in items:
        p = product_by_id.get(i.products_id)
        if not p:
            continue
        out.append(
            {
                "products_id": p.products_id,
                "product_title": p.product_title,
                "product_price": int(p.product_price),
                "product_img1": p.product_img1,
                "qty": int(i.qty),
            }
        )
    return out


def build_base_context(request: Request, db: Session, *, active: str) -> dict[str, Any]:
    customer_email = ensure_session_customer_email(request)
    categories = db.query(Category).order_by(Category.cat_id.asc()).all()
    prod_categories = db.query(ProductCategory).order_by(ProductCategory.p_cat_id.asc()).all()

    totals = get_cart_totals(db, customer_email)
    cart_preview = get_cart_preview_items(db, customer_email, limit=2)

    customer: Customer | None = None
    if is_logged_in(customer_email):
        customer = db.query(Customer).filter(Customer.customer_email == customer_email).first()

    return {
        "request": request,
        "active": active,
        "flash": pop_flash(request),
        "session_customer_email": customer_email,
        "is_logged_in": is_logged_in(customer_email),
        "categories": categories,
        "prod_categories": prod_categories,
        "cart_items_count": totals.items_count,
        "cart_total_price": totals.total_price,
        "cart_preview_items": cart_preview,
        "current_customer": customer,
    }

