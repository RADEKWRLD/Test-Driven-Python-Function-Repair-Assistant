def check_dict_case(dict):
    if len(dict) == 0:
        return False
    keys = dict.keys()
    lowercase_keys = all(key.islower() for key in keys if isinstance(key, str))
    uppercase_keys = all(key.isupper() for key in keys if isinstance(key, str))
    return lowercase_keys or uppercase_keys
