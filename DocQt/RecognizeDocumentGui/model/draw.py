import os
from PIL import Image, ImageDraw

def draw_lines(img, draw, response, pathImage):

    box_color = (255, 0, 0)

    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            geometry = item['Geometry']['BoundingBox']
            width, height = img.size
            left = geometry['Left'] * width
            top = geometry['Top'] * height
            right = (geometry['Left'] + geometry['Width']) * width
            bottom = (geometry['Top'] + geometry['Height']) * height

            draw.rectangle([left, top, right, bottom], outline=box_color, width=3)

    pathImageLines = os.path.join(pathImage, 'output_with_lines.jpg')

    img.save(pathImageLines)

def draw_boxes(img, draw, response, pathImage):
    box_color = (255, 0, 0)

    paragraphs = []
    current_paragraph = []

    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            current_paragraph.append(item)
        else:
            if current_paragraph:
                left = min([line['Geometry']['BoundingBox']['Left'] for line in current_paragraph])
                top = min([line['Geometry']['BoundingBox']['Top'] for line in current_paragraph])
                right = max([line['Geometry']['BoundingBox']['Left'] + line['Geometry']['BoundingBox']['Width'] for line in current_paragraph])
                bottom = max([line['Geometry']['BoundingBox']['Top'] + line['Geometry']['BoundingBox']['Height'] for line in current_paragraph])

                width, height = img.size
                left *= width
                top *= height
                right *= width
                bottom *= height
                draw.rectangle([left, top, right, bottom], outline=box_color, width=2)

                current_paragraph = [] 

    pathImageBoxes = os.path.join(pathImage, 'output_with_boxes.jpg')            
    
    img.save(pathImageBoxes)

def draw_tables(img, draw, response, pathImage):
    box_color = (255, 255, 0)

    for item in response['Blocks']:
        if item['BlockType'] == 'TABLE':
            table_cells = [block for block in response['Blocks'] if block['BlockType'] == 'CELL']
            for cell in table_cells:
                geometry = cell['Geometry']['BoundingBox']
                width, height = img.size
                left = geometry['Left'] * width
                top = geometry['Top'] * height
                right = (geometry['Left'] + geometry['Width']) * width
                bottom = (geometry['Top'] + geometry['Height']) * height

                draw.rectangle([left, top, right, bottom], outline=box_color, width=2)

    pathImageTables = os.path.join(pathImage, 'output_with_tables.jpg')

    img.save(pathImageTables)

# Bisogna ripensare a questa funzione
def draw_boxes_on_image(image_path, response):

    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # draw_tables(img, draw, response)     
