import json


class BaseResponse(object):
    version = '0.0.1'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class QueryResponse(BaseResponse):
    def __init__(self, departure, destination, daystamp, results):
        super(QueryResponse, self).__init__(
            departure=departure,
            destination=destination,
            daystamp=daystamp,
            results=results,
            )


class ResponseJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, BaseResponse):
                return obj.__dict__
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
