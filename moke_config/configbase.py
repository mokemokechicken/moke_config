from copy import copy, deepcopy
from logging import getLogger


logger = getLogger(__name__)


def create_config(cls, config_dict=None):
    config_dict = config_dict or {}
    obj = cls()
    obj._apply(config_dict)
    if hasattr(obj, "_after_apply"):
        # noinspection PyProtectedMember
        obj._after_apply()
    return obj


def to_dict(obj, delete_keys=None):
    """

    :param ConfigBase obj:
    :param delete_keys:
    :return:
    """
    return obj._to_dict(delete_keys=delete_keys)


class ConfigBase:
    def _apply(self, config_dict=None):
        config_dict = config_dict or {}
        assert isinstance(config_dict, dict)

        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue
            value = config_dict.get(k)
            stored_value = config_dict.get(k, v)

            if isinstance(v, type) and issubclass(v, ConfigBase):
                if isinstance(value, dict):
                    stored_value = create_config(v)
                elif k not in config_dict or value is None:
                    stored_value = create_config(v, config_dict)
                else:
                    logger.warning("expected dict like %s but %s" % (v, type(value)))
            elif isinstance(v, list) and len(v) == 1 and isinstance(v[0], type) and issubclass(v[0], ConfigBase):
                if isinstance(value, list):
                    stored_value = [create_config(v[0], x) for x in value]
                elif k not in config_dict or value is None:
                    stored_value = []
                else:
                    logger.warning("expected list of dict like list[%s] but %s" % (v, type(value)))
            elif isinstance(v, ConfigBase):
                if isinstance(value, dict):
                    stored_value = v._apply(value)
                else:
                    stored_value = v

            setattr(self, k, stored_value)

        return self

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def _to_dict(self, delete_keys=None):
        """

        :rtype: dict
        """
        ret = copy(self.__dict__)
        for k, v in list(ret.items()):
            if isinstance(v, ConfigBase):
                ret[k] = v._to_dict(delete_keys=delete_keys)
            elif isinstance(v, list):
                ret[k] = v = copy(v)
                for i, vv in enumerate(v):
                    if isinstance(vv, ConfigBase):
                        v[i] = vv._to_dict(delete_keys=delete_keys)

        ret = deepcopy(ret)

        if delete_keys:
            for k in delete_keys:
                if k in ret:
                    del ret[k]
        return ret


def pprint_config(h):
    if not isinstance(h, ConfigBase):
        return str(h)
    return "\n".join([str((str(k), pprint_config(v))) for k, v in sorted(to_dict(h).items())])

