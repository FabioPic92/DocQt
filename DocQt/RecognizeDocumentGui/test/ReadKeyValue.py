import argparse
import json
import cv2
import boto3

parser = argparse.ArgumentParser(description="Carica un'immagine e un file JSON.")
parser.add_argument('--image', type=str, required=True, help='Path dell\'immagine')

args = parser.parse_args()

textract = boto3.client('textract')

with open(args.image, 'rb') as img_file:
    # Esegui Textract su un'immagine (JPG in questo caso)
    response = textract.analyze_document(
        Document={'Bytes': img_file.read()},
        FeatureTypes=['FORMS']  # Analizza le forme, come i key-value pairs
    )

key_value_pairs = {}

for block in response['Blocks']:
    if block['BlockType'] == 'KEY_VALUE_SET':
        key = None
        value = None

        # Trova la chiave
        for entity in block['EntityTypes']:
            if entity == 'KEY' and 'Key' in block:
                key = block['Key']['Text']  # Estrai il testo della chiave
            elif entity == 'VALUE' and 'Value' in block:
                value = block['Value']['Text']  # Estrai il testo del valore

        # Aggiungi alla mappa dei key-value se entrambi sono trovati
        if key and value:
            key_value_pairs[key] = value

output_json_path = "Test.json"

with open(output_json_path, 'w') as json_file:
    json.dump(response, json_file, indent=4)

if key_value_pairs:
    print("Key-Value Pairs estratti:")
    for key, value in key_value_pairs.items():
        print(f'{key}: {value}')
else:
    print("Nessuna coppia chiave-valore trovata nel documento.")
