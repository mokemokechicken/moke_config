import os
from copy import copy, deepcopy
from logging import getLogger


logger = getLogger(__name__)


class Config:
    @classmethod
    def create(cls, config_dict=None):
        config_dict = config_dict or {}
        obj = cls()
        obj._apply(config_dict)
        if hasattr(obj, "_after_apply"):
            # noinspection PyProtectedMember
            obj._after_apply()
        return obj

    def _apply(self, config_dict=None):
        config_dict = config_dict or {}
        assert isinstance(config_dict, dict)

        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue
            value = config_dict.get(k)
            stored_value = config_dict.get(k, v)

            if isinstance(v, type) and issubclass(v, Config):
                if isinstance(value, dict):
                    stored_value = v.create()
                elif k not in config_dict or value is None:
                    stored_value = v.create(config_dict)
                else:
                    logger.warning("expected dict like %s but %s" % (v, type(value)))
            elif isinstance(v, list) and len(v) == 1 and isinstance(v[0], type) and issubclass(v[0], Config):
                if isinstance(value, list):
                    stored_value = [v[0].create(x) for x in value]
                elif k not in config_dict or value is None:
                    stored_value = []
                else:
                    logger.warning("expected list of dict like list[%s] but %s" % (v, type(value)))
            elif isinstance(v, Config):
                if isinstance(value, dict):
                    stored_value = v._apply(value)
                else:
                    stored_value = v

            if isinstance(stored_value, EnvValue):
                stored_value = stored_value.eval()

            if callable(stored_value):
                stored_value = property(fget=stored_value)
                setattr(self.__class__, k, stored_value)
            else:
                setattr(self, k, stored_value)

        return self

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
                ret[k] = v.to_dict(delete_keys=delete_keys)
            elif isinstance(v, list):
                ret[k] = v = copy(v)
                for i, vv in enumerate(v):
                    if isinstance(vv, Config):
                        v[i] = vv.to_dict(delete_keys=delete_keys)

        ret = deepcopy(ret)

        if delete_keys:
            for k in delete_keys:
                if k in ret:
                    del ret[k]
        return ret


class EnvValue:
    def __init__(self, var_name, default_value=None):
        self.var_name = var_name
        self.default_value = default_value

    def eval(self):
        return os.environ.get(self.var_name, self.default_value)

    def __str__(self):
        return self.eval()


def pprint_config(h):
    if not isinstance(h, Config):
        return str(h)
    return "\n".join([str((str(k), pprint_config(v))) for k, v in sorted(h.to_dict().items())])

