from dataclasses import dataclass


@dataclass
class Product:
    id: int
    title: str
    category: str
    in_stock: int
    color: str | None = None
    size: int | None = None
    description: str | None = None
    image_location: str | None = None
    brand: str | None = None
