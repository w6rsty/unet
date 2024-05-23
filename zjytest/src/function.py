import json
def getJson(file_index):
    with open(f'json/json{file_index}.json', 'r',encoding="utf-8") as f:
        json_data = json.load(f)
    return json_data

    #点击小图片，然后将小图片展示到大屏中，再将患者信息和分析报告展示出来
    #def imageClick(self):
    