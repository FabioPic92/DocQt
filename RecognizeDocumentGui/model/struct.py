from typing import List, Optional
from dataclasses import dataclass
from numpy.typing import NDArray
import numpy as np

@dataclass
class DocumentData:
    filename: Optional[str] = None
    filename_image_processed: Optional[str] = None
    image: Optional[NDArray[np.uint8]] = None
    image_proc: Optional[NDArray[np.uint8]] = None

listModelDocument = [] # Lista che memorizza i modelli dei documenti caricati 