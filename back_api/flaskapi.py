from flask import Flask
from flask_cors import CORS
import json
import sys

app = Flask(__name__)
CORS(app)

id_string = "Id"


with open('phones.json') as phones_json_file:
    phones_loaded = json.load(phones_json_file)

@app.route('/device/all', methods=['GET'])
def get_all_devices():
    return json.dumps(phones_loaded, default=str)


@app.route('/device/<device_id>', methods=['GET'])
def get_specific_device_by_id(device_id):
    for item in phones_loaded:
        if str(item[id_string]) == device_id:
            return json.dumps(item, default=str)
    return "No Device Found"


@app.route('/device/<device_offset>/count/<amount_of_devices>', methods=['GET'])
def get_device_list_from_with_count(device_offset, amount_of_devices):
    returned_device_array = []
    for item in phones_loaded:
        in_search_parameters = int(item[id_string]) > int(device_offset) and int(
            item[id_string]) <= int(device_offset) + int(amount_of_devices)
        if in_search_parameters:
            returned_device_array.append(item)
        out_of_search_parameters = int(item[id_string]) > int(
            device_offset) + int(amount_of_devices)
        if out_of_search_parameters:
            break
    return json.dumps(returned_device_array, default=str)

@app.route('/edge-scores', methods=['GET'])
def get_scores():
    
    returned_edge_scores = {
            'minPerformance': sys.maxsize,
            'topPerformance': 0,
            'minBatteryLife': sys.maxsize,
            'topBatteryLife': 0,
    }
    
    for item in phones_loaded:
        less_preformance = int(item["antutu"]) < int(returned_edge_scores["minPerformance"]) 
        if less_preformance:
            returned_edge_scores["minPerformance"] = item["antutu"];
        
        better_preformance = int(item["antutu"]) > int(returned_edge_scores["topPerformance"])
        if better_preformance:
            returned_edge_scores["topPerformance"] = item["antutu"];
          
            
        less_batterylife = int(item["batterylife"]) < int(returned_edge_scores["minBatteryLife"]) 
        if less_batterylife:
            returned_edge_scores["minBatteryLife"] = item["batterylife"];
        
        better_batterylife = int(item["batterylife"]) > int(returned_edge_scores["topBatteryLife"])
        if better_batterylife:
            returned_edge_scores["topBatteryLife"] = item["batterylife"];
            
    return json.dumps(returned_edge_scores, default=str)


if __name__ == "__main__":
    app.run()
