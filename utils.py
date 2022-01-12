import toml
import sys

def contains_key(_json, key):
    path = key
    if isinstance(key, str):
        path = key.split('.')
    if type(_json) is dict:
        for _json_key in (_json):
            if _json_key == path[0] and len(path) == 1:
                val = _json[_json_key]
                return val
            elif _json_key == path[0] and type(_json[_json_key]) in (list, dict):
                path.pop(0)
                return contains_key(_json[_json_key], path)
    elif type(_json) is list:
        for item in _json:
            if type(item) in (list, dict):
                search(item, key)

class Dict2Obj:

    def __init__(self, d={}):
        for k, v in d.items():
            if isinstance(v, dict):
                setattr(self, k, Dict2Obj(d=v))
            else:
                setattr(self, k, v)

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self):
        return "{}".format(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()

class Config(Dict2Obj):

    def __init__(self, args):
        toml_config = toml.load(args['config']) if args['config'] else {}
        keys_not_found = []

        for key, value in args.items():
            path = key.split('.')
            if len(path) != 0 and path[0] == 'app':
                key_path = path[1]
                if not value:
                    value = contains_key(toml_config, key)
                    if not value:
                        keys_not_found.append(key)
                    continue
                toml_config['app'][key_path] = value
        if keys_not_found:
            for key in keys_not_found:
                print('{} not found'.format(key))
            print("Please set the values above either ine the config file or as parameters to the command.")
            sys.exit(1)
        super().__init__(toml_config)


class Status:
    error = 0
    redl = 0
    dls = 0
    total = 0
    gif = 0
    video = 0
    photo = 0

    def __str__(self):
        return 'GIF: {}; VIDEO; {}; PHOTO: {}\nDL: {}; REDL: {}; ERROR: {}; TOTAL: {}'.format(
            self.gif, self.video, self.photo, self.dls, self.redl, self.error, self.total)

