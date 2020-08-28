import functools
import os
import json
import base64


class Cachefy:

    @staticmethod
    def cache_dict_of_dicts(DIR):
        def cache(method):
            @functools.wraps(method)
            def wrapper(self, *args, **kwargs):
                if not os.path.exists(DIR):
                    os.makedirs(DIR)
                target = DIR + '/' + Cachefy.base64encode(f'{method.__name__}_{self.city}') + '.cache'

                def read(target_):
                    with open(target_, 'r') as f:
                        res_ = json.loads(f.read())
                    return res_

                def write(target_, result_):
                    with open(target_, 'w') as f:
                        res_ = json.dumps(result_, indent=1)
                        f.write(res_)
                    return result_

                if os.path.isfile(target):
                    result = read(target)
                    result = {int(key): {int(key_): value_ for key_, value_ in value.items()} for key, value in
                              result.items()}
                else:
                    result = method(self, *args, **kwargs)
                    result = write(target, result)

                return result
            return wrapper
        return cache

    @staticmethod
    def base64encode(string):
        b = string.encode("UTF-8")
        e = base64.b64encode(b)
        encoded = e.decode("UTF-8")
        return encoded

    @staticmethod
    def base64decode(string):
        b1 = string.encode("UTF-8")
        d = base64.b64decode(b1)
        decoded = d.decode("UTF-8")
        return decoded

