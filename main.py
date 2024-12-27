# main.py
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.openapi.models import License
from pydantic import BaseModel, AnyUrl, Field

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
    barcode: str = Field(..., description="Código de barras para buscar en Google")

class BarcodeResult(BaseModel):
    title: str
    link: str
    snippet: str
    date: Optional[str] = None

@app.post("/search-barcode/", response_model=List[BarcodeResult], tags=["Search Barcode"])
def search_barcode(request: BarcodeRequest):
    """
    Busca un producto por código de barras y devuelve los primeros resultados.

    - **barcode**: El código de barras a buscar.
    """
    scraper = BarcodeScraper()
    result = scraper.search_barcode(request.barcode)

    if result:
        return result

    raise HTTPException(status_code=404, detail="No results found")


