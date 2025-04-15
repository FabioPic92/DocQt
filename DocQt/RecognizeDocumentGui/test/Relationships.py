import json

# Carica il file JSON
with open('Test.json', 'r') as f:
    data = json.load(f)

# Lista per raccogliere tutti gli ID delle relationships dei blocchi KEY
relationship_ids = []

# Itera su tutti i blocchi
for block in data.get('Blocks', []):
    if block.get('BlockType') == 'KEY_VALUE_SET' and 'KEY' in block.get('EntityTypes', []):
        for relationship in block.get('Relationships', []):
            if relationship.get('Type') == 'VALUE':  # puoi anche controllare per 'CHILD' se serve
                ids = relationship.get('Ids', [])
                relationship_ids.extend(ids)  # Aggiungi gli ID alla lista

print("IDs delle relationships di tipo VALUE:")
print(relationship_ids)