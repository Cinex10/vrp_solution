import json

def fetch_wilayas():
    file_path = 'data/dz.json'
    with open(file_path,'r') as file:
        fileData  = file.read()
        jsonData = json.loads(fileData)
        data = {}
        for entry in jsonData:
            data.update(
                {
                    entry['city'] : [entry['lat'],entry['lng']],
                }
            )
        return data












