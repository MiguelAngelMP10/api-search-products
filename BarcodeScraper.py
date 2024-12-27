import requests
from bs4 import BeautifulSoup
import random


class BarcodeScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            ]),
            "Accept-Language": "en-US,en;q=0.9",
        }

    def search_barcode(self, barcode):
        """Busca un código de barras en Google y devuelve los resultados."""
        url = f"https://www.google.com/search?q={barcode}"
        print(f"Buscando el código de barras: {barcode}...\n")

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return []

        # Analizar el contenido HTML
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        # Extraer información de resultados
        for g in soup.select(".tF2Cxc"):
            try:
                title = g.select_one("h3").text
                link = g.select_one("a")["href"]
                snippet = g.select_one(".VwiC3b").text
                results.append({"title": title, "link": link, "snippet": snippet})
            except AttributeError:
                continue

        return results

    def get_first_result(self, barcode):
        """Obtiene la información del primer resultado de búsqueda."""
        results = self.search_barcode(barcode)

        if results:
            return results[0]
        else:
            return []
