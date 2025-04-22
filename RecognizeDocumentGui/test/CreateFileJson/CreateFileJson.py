import json
import boto3
import cv2

error = 0.002

textract = boto3.client('textract')

# with open("Test2.jpg", 'rb') as img_file:
#     response = textract.analyze_document(
#         Document={'Bytes': img_file.read()},
#         FeatureTypes=['FORMS', 'TABLES'] 
#     )

# with open("response.json", "w") as outfile:
#     json.dump(response, outfile, indent=4)


polygons = []
for block in response.get("Blocks", []):
    if block.get("BlockType") == "LINE":
        geometry = block.get("Geometry", {})
        polygon = geometry.get("Polygon", [])
        if polygon:
            polygons.append(polygon)    

with open("line_polygons.json", "w") as outfile:
    json.dump(polygons, outfile, indent=4)

