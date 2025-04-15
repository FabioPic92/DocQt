import os
import json
from PDF import PDF

output_file_path = 'output.txt' 

# search Block Page in json image
def search_block_page(data):
    page_blocks = [block for block in data["Blocks"] if block["BlockType"] == "PAGE"]

# search Block Line in json image
def search_block_lines(data):
    line_blocks = [block for block in data["Blocks"] if block["BlockType"] == "LINE"]
    return line_blocks

# Convert Json in a vector
def search_ids(data):
    page_ids = [relationship["Ids"] for block in data["Blocks"] 
            if block["BlockType"] == "PAGE" and "Relationships" in block
            for relationship in block["Relationships"] if "Ids" in relationship]

    flat_page_ids = [item for sublist in page_ids for item in sublist]
    print(len(flat_page_ids))
    return flat_page_ids 

# Print number of blocks
def print_text_of_lines_matching_ids(data, page_ids):
    count = 0
    for block in data["Blocks"]:
        for block["Id"] in page_ids:
            print(block["BlockType"])
            count = count + 1
    print(count)

# Da sistemare
def AnalyzeDocument(pathFile, nameFile):
    # pathFile contiete il percorso alla cartella dove avviene il test
    jsonFile = nameFile + '.json'
    pdfFile = nameFile + '.pdf'
    textFile = nameFile + '.txt'

    pathJson = os.path.join(pathFile, 'Json', jsonFile)
    pathPdf = os.path.join(pathFile, 'Pdf', pdfFile)
    pathText = os.path.join(pathFile, 'Text', textFile)

    with open(pathJson, 'r') as file:
        data = json.load(file)

    line_blocks = search_block_lines(data)

    data_sort = sorted(line_blocks, key=lambda x: x['Geometry']['BoundingBox']['Top'])

    pdf = PDF(pathPdf)

    # size horizontal == 600 and Vertical == 780
    for item in  data_sort:
        pdf.setText((item['Geometry']['BoundingBox']['Left']) * 600, (1-item['Geometry']['BoundingBox']['Top']) * 780, item['Text'])
    
    pdf.savePdf()    

    lines = []
    for block in data['Blocks']:
        if block['BlockType'] == 'LINE':
            text = block['Text']
            top = block['Geometry']['BoundingBox']['Top']
            left = block['Geometry']['BoundingBox']['Left']
            width = block['Geometry']['BoundingBox']['Width']
            height = block['Geometry']['BoundingBox']['Height']
            lines.append({'text': text, 'top': top, 'left': left, 'width': width, 'height': height})

    lines = sorted(lines, key=lambda x: x['top'])

    with open(pathText, 'w') as output_file:
        previous_top = lines[0]['top']
        for line in lines:

            if line['top'] > previous_top + 0.01:  
                output_file.write('\n')
            output_file.write(line['text'] + ' ')
            previous_top = line['top']

    # with open(pathText, 'w') as output_file:
    #     previous_item = data_sort[0]
    #     for item in data_sort:
    #         if item['Geometry']['BoundingBox']['Left'] < previous_item['Geometry']['BoundingBox']['Left']:
    #             output_file.write(json.dumps(item["Text"]) + '\n') #togliere json.dumps
    #         else:
    #             output_file.write(json.dumps(item["Text"]))
    #         previous_item = item