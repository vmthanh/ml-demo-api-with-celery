import six


class TypeUtils(object):

    INTEGER_TYPES = six.integer_types
    NUMBER_TYPES = tuple(list(six.integer_types) + [float])

    @classmethod
    def is_bool(cls, obj):
        return isinstance(obj, bool)

    @classmethod
    def is_int(cls, obj):
        return isinstance(obj, cls.INTEGER_TYPES) and not isinstance(obj, bool)

    @classmethod
    def is_number(cls, obj):
        return isinstance(obj, cls.NUMBER_TYPES) and not isinstance(obj, bool)

    @classmethod
    def as_type(cls, obj, default, _type):
        try:
            return _type(obj)
        except (ValueError, TypeError):
            return default

    @classmethod
    def as_int(cls, obj, default):
        return cls.as_type(obj, default, int)

    @classmethod
    def as_float(cls, obj, default):
        return cls.as_type(obj, default, float)

    @classmethod
    def as_number(cls, obj, default):
        return cls.as_float(obj, default)

    @classmethod
    def as_str(cls, obj, default):
        try:
            # pylint: disable=consider-using-f-string
            return "%s" % obj
        except (ValueError, TypeError):
            return default

    @classmethod
    def as_str_list(cls, raw_list):
        """
        :type raw_list: list or tuple
        :rtype: list
        """
        # pylint: disable=consider-using-f-string
        return ["%s" % v for v in raw_list or []]
