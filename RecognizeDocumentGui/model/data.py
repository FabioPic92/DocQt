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

error = 0.02

P1_x = 0.04616007208824158
P1_y = 0.2436360865831375
P2_x = 0.3395560383796692
P2_y = 0.2930818498134613

P3_x = 0.9303025007247925
P3_y = 0.8902167677879333
P4_x = 0.1115032434463501
P4_y = 0.9041821956634521

P5_x = 0.7805507183074951
P5_y = 0.9298563003540039
P6_x = 0.9161749482154846
P6_y = 0.9413824081420898
