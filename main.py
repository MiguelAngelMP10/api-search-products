# main.py
from fastapi import FastAPI
from fastapi.openapi.models import License
from pydantic import BaseModel, AnyUrl

from BarcodeScraper import BarcodeScraper

# Crear la instancia de la aplicación
app = FastAPI(
    title="Mi API de para buscar productos por codigo de barras en google",
    description="Esta es una API de para buscar productos por codigo de barras en google",
    version="1.0.0",
    docs_url="/docs",  # URL donde estará la documentación Swagger
    redoc_url="/redoc",  # URL donde estará la documentación ReDoc
    contact={
        "name": "Miguel Ángel Muñoz Pozos",
        "email": "mmunozpozos@gmail.com"
    },
    license=License(name="MIT", url=AnyUrl("https://opensource.org/licenses/MIT")),
)


# Definir el modelo para la entrada y salida de datos
class BarcodeRequest(BaseModel):
    barcode: str


@app.post("/search-barcode/", tags=["Search Barcode"])
def search_barcode(request: BarcodeRequest):
    scraper = BarcodeScraper()
    result = scraper.search_barcode(request.barcode)
    if result:
        return result
    return {"message": "No results found"}
