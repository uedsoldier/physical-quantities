import json

def json_to_dict(json_file, encoding='utf-8') -> dict:
    """Converts a json object from a path to a python dict

    Args:
        json_file (str): Path to the json file
        encoding (str, optional): Encoding of the file. Defaults to 'utf-8'.

    Returns:
        dict: Dictionary with json content from file
    """
    with open(json_file,'r', encoding=encoding) as file:
        return json.load(file)

    
def json_string_to_dict(json_string):
    return json.loads(json_string)


def dict_to_json(dict,json_file, ensure_ascii=False):
    with open(json_file,'w') as file:
        json.dump(dict,file,ensure_ascii=ensure_ascii)
        
def dict_to_json_string(dict, ensure_ascii=False):
    return json.dumps(dict,ensure_ascii=ensure_ascii)