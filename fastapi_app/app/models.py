from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Integer, Text, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Category(Base):
    __tablename__ = "category"

    cat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cat_title: Mapped[str] = mapped_column(Text)
    cat_desc: Mapped[str] = mapped_column(Text)


class ProductCategory(Base):
    __tablename__ = "product_categories"

    p_cat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    p_cat_title: Mapped[str] = mapped_column(Text)
    p_cat_desc: Mapped[str] = mapped_column(Text)


class Product(Base):
    __tablename__ = "products"

    products_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    p_cat_id: Mapped[int] = mapped_column(Integer)
    cat_id: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    product_title: Mapped[str] = mapped_column(Text)
    product_img1: Mapped[str] = mapped_column(Text)
    product_img2: Mapped[str] = mapped_column(Text)
    product_price: Mapped[int] = mapped_column(Integer)
    product_keywords: Mapped[str] = mapped_column(Text)
    product_desc: Mapped[str] = mapped_column(Text)


class Slider(Base):
    __tablename__ = "slider"

    slide_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slide_name: Mapped[str] = mapped_column(String(255))
    slide_image: Mapped[str] = mapped_column(Text)
    slide_heading: Mapped[str] = mapped_column(String(100))
    slide_text: Mapped[str] = mapped_column(String(100))


class Customer(Base):
    __tablename__ = "customer"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(255))
    customer_email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    customer_pass: Mapped[str] = mapped_column(String(50))
    customer_address: Mapped[str] = mapped_column(String(400))
    customer_contact: Mapped[str] = mapped_column(Text)
    customer_image: Mapped[str] = mapped_column(Text)
    customer_ip: Mapped[int] = mapped_column(Integer)


class CartItem(Base):
    __tablename__ = "cart"

    # En el PHP se evita duplicar productos por c_id, así que usamos PK compuesta.
    products_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    c_id: Mapped[str] = mapped_column(String(255), primary_key=True)

    ip_add: Mapped[str] = mapped_column(String(255))
    qty: Mapped[int] = mapped_column(Integer)
    size: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_qty: Mapped[int] = mapped_column(Integer)
    order_price: Mapped[int] = mapped_column(Integer)
    c_id: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

