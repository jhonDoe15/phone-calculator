import pandas
from datetime import datetime, timedelta
import flask
import json
import time


app = flask.Flask(__name__)
app.config["DEBUG"] = True

df = pandas.read_csv('gsm.csv', usecols=['oem', 'model', 'body_weight', 'display_size', 'sound_3.5mm_jack', 'launch_announced'], header=0, dtype={
                     "model": "string", "launch_announced": "string"})

dates = df["launch_announced"]
models = df["model"]
oems = df["oem"]
weights = df["body_weight"]
display_sizes = df["display_size"]
jacks = df["sound_3.5mm_jack"]
applicable_devices_count = 0
devices_json = []
for i in range(len(df)):
    no_good_device_date = False
    current_date = dates[i]
    no_comma_date_string = current_date[:4] + current_date[5:]
    try:
        date_type_release_date = datetime.strptime(
            no_comma_date_string, '%Y %B %d')
        # print(date_type_release_date)
    except:
        try:
            date_type_release_date = datetime.strptime(
                no_comma_date_string, '%Y %B')
            # print(date_type_release_date)
        except:
            try:
                date_type_release_date = datetime.strptime(
                    no_comma_date_string, '%Y %b')
                # print(date_type_release_date)
            except:
                no_good_device_date = True

    good_device_date = not no_good_device_date

    if good_device_date:

        is_device_date_relevant = date_type_release_date >= (
            datetime.now() - timedelta(days=730))

        if is_device_date_relevant:
            current_model = models[i]
            jack_presence = True if jacks[i] == "Yes" else False
            devices_json.append(
                {
                    'ID': applicable_devices_count,
                    'brand': oems[i],
                    'model': models[i],
                    'release_date': date_type_release_date,
                    'weight': weights[i],
                    'display_size': display_sizes[i].split(",")[0],
                    'jack_present': jack_presence,
                }
            )
            applicable_devices_count += 1

@app.route('/device/all', methods=['GET'])
def get_all_devices():
    return json.dumps(devices_json, default=str)

@app.route('/device/<device_id>', methods=['GET'])
def get_specific_device_by_id(device_id):
    for item in devices_json:
        if str(item["ID"]) == device_id:
            return json.dumps(item, default=str)
    return "No Device Found";

@app.route('/device/<device_offset>/count/<amount_of_devices>', methods=['GET'])
def get_device_list_from_with_count(device_offset, amount_of_devices):
    returned_device_array = []
    for item in devices_json:
        if item["ID"] > int(device_offset) and item["ID"] <= int(device_offset) + int(amount_of_devices):
            returned_device_array.append(item)
        out_of_search_parameters = item["ID"] > int(device_offset) + int(amount_of_devices)
        if out_of_search_parameters:
            break
    return json.dumps(returned_device_array, default=str)




if __name__ == "__main__":
    app.run()
