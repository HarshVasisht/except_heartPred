import json, os

# traceback.install()
# console
def read_data(f_name):
    # Opening JSON file
    if not os.path.exists(f_name):
        return {}
    
    f = open(f_name)

    # returns JSON object as a dictionary
    data = json.load(f)

    
    # Closing file
    f.close()
    return data

def write_data(data, f_name):
    json_object = json.dumps(data, indent=4)
 
    # Writing to sample.json
    with open(f_name, "w+") as outfile:
        outfile.write(json_object)
