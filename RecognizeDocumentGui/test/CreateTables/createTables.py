import argparse
import boto3
import cv2
import json
from typing import Optional
from dataclasses import dataclass

@dataclass
class Point:
    x: Optional[float] = None
    y: Optional[float] = None

@dataclass
class DataTable:
    p1: Optional[Point] = None
    p2: Optional[Point] = None
    p3: Optional[Point] = None    
    p4: Optional[Point] = None

def collect_words_from_key_value_set(block_id, blocks_map):
    """
    Estrae tutti i blocchi WORD discendenti da un blocco KEY_VALUE_SET, anche se annidati.
    :param block_id: ID del blocco KEY_VALUE_SET di partenza
    :param blocks_map: dizionario {block_id: block}
    :return: lista di blocchi WORD
    """
    words = []

    def traverse(block_id):
        block = blocks_map.get(block_id)
        if not block or 'Relationships' not in block:
            return

        for relation in block['Relationships']:
            if relation['Type'] == 'CHILD':
                for child_id in relation['Ids']:
                    child = blocks_map.get(child_id)
                    if not child:
                        continue
                    if child['BlockType'] == 'WORD':
                        words.append(child)
                    elif child['BlockType'] == 'LINE':
                        # opzionale: raccogli anche LINE
                        pass
                    elif child['BlockType'] == 'KEY_VALUE_SET':
                        traverse(child_id)  # ricorsione su blocchi annidati

            elif relation['Type'] == 'VALUE':
                for value_id in relation['Ids']:
                    traverse(value_id)  # continua ricorsione

    traverse(block_id)
    return words

def find_parent_key(key_id, blocks_map):
    list = []

    for block in blocks_map.values():
        if block["BlockType"] != "KEY_VALUE_SET":
            continue
        print(block["Id"])
        for rel in block.get("Relationships", []):
            print(rel["Type"])
            if block.get("EntityTypes") == ["KEY"] and rel["Type"] == "CHILD":
                rr = rel
                for r in rr.get("Ids", []):
                    print(r)
                    

    # for block in blocks_map.values():
    #     if block["BlockType"] != "KEY_VALUE_SET":
    #         continue
    #     if block.get("EntityTypes") != ["KEY"]:
    #         continue
    #     for rel in block.get("Relationships", []):
    #         if rel["Type"] == "VALUE":
    #             for value_id in rel["Ids"]:
    #                 value_block = blocks_map.get(value_id)
    #                 if not value_block:
    #                     continue
    #                 for subrel in value_block.get("Relationships", []):
    #                     if subrel["Type"] == "CHILD" and key_id in subrel["Ids"]:
    #                         return block  # questo è il "padre" del key_id
    return None

parser = argparse.ArgumentParser(description="Carica un'immagine e un file JSON.")
parser.add_argument('--image', type=str, required=True, help='Path dell\'immagine')
parser.add_argument('--json', type=str, required=True, help='Path del file JSON')

args = parser.parse_args()

with open(args.json, 'r') as f:
    data = json.load(f)

blocks_map = {b['Id']: b for b in data['Blocks']}

# Esempio: ID di un blocco KEY_VALUE_SET (KEY)
key_block_id = "2a971150-e586-4168-ba5f-95b5a13cbfb1"

w = find_parent_key(key_block_id, blocks_map)

#words = collect_words_from_key_value_set(key_block_id, blocks_map)

#for word in words:
#    print(word['Text'], word['Geometry']['BoundingBox'])    


