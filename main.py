import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

class YouTubeClickbaitDetector:
    def __init__(self, url):
        self.url = url
        self.video_id = self.extraer_id_video()
        self.titulo = None
        self.ruta_miniatura = None

    def extraer_id_video(self):
        parsed_url = urlparse(self.url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
            if parsed_url.path[:7] == '/embed/':
                return parsed_url.path.split('/')[2]
            if parsed_url.path[:3] == '/v/':
                return parsed_url.path.split('/')[2]
        return None

    def obtener_titulo(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.titulo = soup.find('title').text.replace(' - YouTube', '')

    def descargar_miniatura(self):
        if not self.video_id:
            print("No se pudo extraer el ID del video.")
            return

        url = f"https://img.youtube.com/vi/{self.video_id}/sddefault.jpg"
        response = requests.get(url)
        if response.status_code == 200:
            self.ruta_miniatura = f"tmp/{self.video_id}.jpg"
            with open(self.ruta_miniatura, "wb") as file:
                file.write(response.content)
        else:
            print("No se pudo descargar la miniatura")

    def procesar(self):
        if not self.video_id:
            print("No se pudo extraer el ID del video de la URL proporcionada.")
            return

        self.obtener_titulo()
        self.descargar_miniatura()

        print(f"Título del video: {self.titulo}")
        print(f"Miniatura descargada como: {self.ruta_miniatura}")

def main():
    parser = argparse.ArgumentParser(description="Detector de clickbait en YouTube")
    parser.add_argument("--url", required=True, help="URL del video de YouTube")
    args = parser.parse_args()

    detector = YouTubeClickbaitDetector(args.url)
    detector.procesar()

if __name__ == "__main__":
    main()
