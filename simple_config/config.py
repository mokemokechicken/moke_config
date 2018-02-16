from copy import copy
from logging import getLogger


logger = getLogger(__name__)


class Config:
    def __init__(self, **kwargs):
        if kwargs:
            self._set_dict_value(kwargs)

    def _set_dict_value(self, config_dict):
        assert isinstance(config_dict, dict)

        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue
            saved_value = config_dict.get(k, v)

            if issubclass(v, Config):
                value = config_dict.get(k)
                if isinstance(value, dict):
                    saved_value = v(value)
                elif isinstance(value, list):
                    saved_value = [v(x) for x in value]
                elif k not in config_dict or value is None:
                    saved_value = v()
                else:
                    logger.warning("expected dict like %s but %s" % (v, type(value)))
            elif isinstance(v, Config):
                value = config_dict.get(k)
                if isinstance(value, dict):
                    v._set_dict_value(value)
                    saved_value = v
                else:
                    saved_value = v
            setattr(self, k, saved_value)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def to_dict(self, delete_keys=None):
        """

        :rtype: dict
        """
        ret = copy(self.__dict__)
        for k, v in list(ret.items()):
            if isinstance(v, Config):
                ret[k] = v.to_dict()

        if delete_keys:
            for k in delete_keys:
                if k in ret:
                    del ret[k]
        return ret


def pprint_config(h):
    if not isinstance(h, Config):
        return str(h)
    return "\n".join([str((str(k), pprint_config(v))) for k, v in sorted(h.to_dict().items())])

