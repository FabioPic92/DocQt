from typing import List
from PIL import Image
from typing import Optional
from dataclasses import dataclass

class DocumentData:
    filename: Optional[str] = None
    image: Optional[Image.Image] = None
    ocr_text: Optional[str] = None

listModelDocument = [] # Lista che memorizza i modelli dei documenti caricati 