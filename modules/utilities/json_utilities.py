import json

def json_to_dict(json_file, encoding='utf-8'):
    try:
        with open(json_file,'r', encoding=encoding) as file:
            return json.load(file)
    except Exception as e:
        raise e


def dict_to_json(dict,json_file, ensure_ascii=False):
    with open(json_file,'w') as file:
        json.dump(dict,file,ensure_ascii=ensure_ascii)
        
def dict_to_json_string(dict, ensure_ascii=False):
    return json.dumps(dict,ensure_ascii=ensure_ascii)