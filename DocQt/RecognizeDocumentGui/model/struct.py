from typing import List
from PIL import Image
from typing import Optional
from dataclasses import dataclass

@dataclass
class DocumentData:
    filename: Optional[str] = None
    image: Optional[Image.Image] = None
    image_proc: Optional[Image.Image] = None

listModelDocument = [] # Lista che memorizza i modelli dei documenti caricati 