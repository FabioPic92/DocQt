import os
import sys
import boto3
import json
import time
import pandas as pd
from PIL import Image, ImageDraw
from AnalyzeDocument import AnalyzeDocument

pathData = "../Data"
pathDataset = "../Data/Dataset"

pathImage = ""
pathJson = ""
pathCsv = ""
pathText = ""
pathPdf = ""

def CreateTestFolder(pathTest, pathTestObj):
    TestPath = os.path.join(pathData, pathTest, pathTestObj)
    os.makedirs(TestPath, exist_ok=False)
    return TestPath

# def draw_lines(img, draw, response):

#     box_color = (255, 0, 0)

#     for item in response['Blocks']:
#         if item['BlockType'] == 'LINE':
#             geometry = item['Geometry']['BoundingBox']
#             width, height = img.size
#             left = geometry['Left'] * width
#             top = geometry['Top'] * height
#             right = (geometry['Left'] + geometry['Width']) * width
#             bottom = (geometry['Top'] + geometry['Height']) * height

#             draw.rectangle([left, top, right, bottom], outline=box_color, width=3)

#     pathImageLines = os.path.join(pathImage, 'output_with_lines.jpg')

#     img.save(pathImageLines)

# def draw_boxes(img, draw, response):
#     box_color = (255, 0, 0)

#     paragraphs = []
#     current_paragraph = []

#     for item in response['Blocks']:
#         if item['BlockType'] == 'LINE':
#             current_paragraph.append(item)
#         else:
#             if current_paragraph:
#                 left = min([line['Geometry']['BoundingBox']['Left'] for line in current_paragraph])
#                 top = min([line['Geometry']['BoundingBox']['Top'] for line in current_paragraph])
#                 right = max([line['Geometry']['BoundingBox']['Left'] + line['Geometry']['BoundingBox']['Width'] for line in current_paragraph])
#                 bottom = max([line['Geometry']['BoundingBox']['Top'] + line['Geometry']['BoundingBox']['Height'] for line in current_paragraph])

#                 width, height = img.size
#                 left *= width
#                 top *= height
#                 right *= width
#                 bottom *= height
#                 draw.rectangle([left, top, right, bottom], outline=box_color, width=2)

#                 current_paragraph = [] 

#     pathImageBoxes = os.path.join(pathImage, 'output_with_boxes.jpg')            
    
#     img.save(pathImageBoxes)

# def draw_tables(img, draw, response):
#     box_color = (255, 255, 0)

#     for item in response['Blocks']:
#         if item['BlockType'] == 'TABLE':
#             table_cells = [block for block in response['Blocks'] if block['BlockType'] == 'CELL']
#             for cell in table_cells:
#                 geometry = cell['Geometry']['BoundingBox']
#                 width, height = img.size
#                 left = geometry['Left'] * width
#                 top = geometry['Top'] * height
#                 right = (geometry['Left'] + geometry['Width']) * width
#                 bottom = (geometry['Top'] + geometry['Height']) * height

#                 draw.rectangle([left, top, right, bottom], outline=box_color, width=2)

#     pathImageTables = os.path.join(pathImage, 'output_with_tables.jpg')

#     img.save(pathImageTables)

# def draw_boxes_on_image(image_path, response):

#     img = Image.open(image_path)
#     draw = ImageDraw.Draw(img)

#     draw_tables(img, draw, response)    


def main():

    start_time = time.time()

    if len(sys.argv) > 1:
        pathTest = sys.argv[1]
        fileTest = sys.argv[2]
    else: 
        print("Error number input file")
        os._exit(1) 

    TestImage = os.path.join(pathDataset, fileTest)

    if not os.path.exists(TestImage):
        print("File not found, abort")
        sys.exit(1) 

    global pathImage
    pathImage = CreateTestFolder(pathTest, "Image")
    global pathJson
    pathJson = CreateTestFolder(pathTest, 'Json')
    global pathCsv
    pathCsv = CreateTestFolder(pathTest, "csv")
    global pathText
    pathText = CreateTestFolder(pathTest, "Text")
    global pathPdf
    pathPdf = CreateTestFolder(pathTest, "Pdf")
    
    textract = boto3.client('textract')

    s3 = boto3.client('s3')
    s3.upload_file(TestImage, 'textextractbucket2', pathTest)

    response = textract.start_document_analysis( 
        DocumentLocation={'S3Object': {'Bucket': 'textextractbucket2', 'Name': pathTest}},
        FeatureTypes=["TABLES", "FORMS"]
    )

    print(response)

    job_id = response['JobId']
    print(f"Job ID: {job_id}")

    while True:
        result = textract.get_document_analysis(JobId=job_id)
        
        if result['JobStatus'] in ['SUCCEEDED', 'FAILED']:
            break
        
        print("In attesa di completamento del lavoro...")
        time.sleep(5)

    print("Documento analizzato")    

    text = ''
    if result['JobStatus'] == 'SUCCEEDED':
        for item in result['Blocks']:
            if item['BlockType'] == 'LINE':
                text = text + " " + item['Text']

    else:
        print(f"Analisi fallita: {result.get('ErrorMessage', 'Nessun errore specificato')}")

    if not fileTest.lower().endswith('.pdf') and not fileTest.lower().endswith('.png'):
        draw_boxes_on_image(TestImage, result)


    comprehend_client = boto3.client('comprehend')

    responseCom = comprehend_client.detect_entities(Text=text, LanguageCode='it')

    TestCsv = os.path.join(pathCsv, 'Test.csv')  

    df = pd.DataFrame(responseCom['Entities'])
    df.to_csv(TestCsv, index=False)

    fileJson = pathTest + '.json'

    TestJson = os.path.join(pathJson, fileJson)

    with open(TestJson, 'w') as json_file:
        json.dump(result, json_file, indent=4)
    

    TestPath = os.path.join(pathData, pathTest)
    AnalyzeDocument(TestPath, pathTest)

    execution_time = time.time() - start_time
    print(f"Tempo di esecuzione: {execution_time} secondi")

if __name__ == '__main__':
    main()