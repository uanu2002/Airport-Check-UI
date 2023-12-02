from flask import Flask, jsonify
from flask_cors import CORS
import json
# import cv2
from PIL import Image

app = Flask(__name__)
CORS(app)

def extract_filename(input_string):
    last_slash_index = input_string.rfind('/')
    if last_slash_index != -1:
        result = input_string[last_slash_index + 1:]
        return result
    else:
        return input_string

def crop_and_save(image_path, value, sub_id):
    # original_image = cv2.imread(image_path)
    x = value["x"]
    y = value["y"]
    width = value["width"]
    height = value["height"]
    original_image = Image.open(f"I:/desktop/UI/Backen/data/{image_path}")
    original_width, original_height = original_image.size
    pixel_x = x / 100.0 * original_width
    pixel_y = y / 100.0 * original_height
    pixel_width = width / 100.0 * original_width
    pixel_height = height / 100.0 * original_height
    
    # cropped_image = original_image[y:y+height, x:x+width]
    print(width)
    cropped_image = original_image.crop((pixel_x, pixel_y, pixel_x + pixel_width, pixel_y + pixel_height))
    sub_name = image_path[:-4] + "_sub_" + str(sub_id) + '.jpg'
    cropped_image.save(f'I:/desktop/UI/Backen/data/{sub_name}')
    # cv2.imwrite(f'I:/desktop/Backen/data/{sub_name}', cropped_image)
    return sub_name


def generate_info_list(path,id=1):
    info_list = []
    with open(path, 'r') as file:
        data = json.load(file)
    annotations = data[id]["annotations"][0]["result"]
    origin_path = data[id]["data"]["image"]
    origin_path = extract_filename(origin_path)
    sub_id = 0
    for relation in annotations:
        if relation["type"]=="relation":
            info = {}
            from_id = relation["from_id"]
            to_id = relation["to_id"]
            for annotation in annotations:
                if annotation["type"] == "rectanglelabels" and (annotation["id"] == from_id or annotation["id"] == to_id):
                    value = annotation["value"]
                    cropped_path = crop_and_save(origin_path, value, sub_id)
                    sub_id += 1
                    if value["rectanglelabels"][0] == "person":
                        info["person"] = cropped_path
                    else:
                        info["object"] = cropped_path
            info_list.append(info)
            info_list.append(info)
            info_list.append(info)
            info_list.append(info)
    return origin_path, info_list

# 路由处理函数，返回infoList数据
@app.route('/get_info_list', methods=['GET'])
def get_info_list():
    test = {
            'origin_path': './g1.png',
            'info_list': [
                {
                    'person': {},
                    'object': {},
                }
            ]
        }
    origin_path, info_list = generate_info_list('./res.json')
    res = {
        'origin_path': origin_path,
        'info_list': info_list,
    }
    # print(res)
    # for _ in range(100):
    #     info_list.append(test)

    return jsonify(result=res)

if __name__ == '__main__':
    app.run(debug=True)
