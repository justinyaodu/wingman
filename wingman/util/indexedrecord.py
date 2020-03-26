from collections import defaultdict

class IndexedRecordMeta(type):
    """Metaclass which adds class variables unique to each subclass of
    IndexedRecord.
    """
    def __new__(class_, name, bases, dict_):
        subclass = super().__new__(class_, name, bases, dict_)

        # map attribute values to subclass instances
        # indexed by [attr_name][attr_value]
        subclass._instances = defaultdict(dict)

        # names of indexed attributes (specified by subclasses)
        subclass._indexed_attr_names = []

        # functions to create new instances from an attribute value
        # (used when a lookup fails because no corresponding instance exists)
        subclass._create_from_attr = {}

        return subclass

class IndexedRecord(metaclass=IndexedRecordMeta):
    """A base class which implements functionality for indexing class
    instances by their attribute values.
    """

    @classmethod
    def _get_by_attr(subclass, attr_name, attr_value, create_if_absent=True):
        """Return the subclass instance which corresponds to a value of
        ``attr_value`` for the attribute specified by ``attr_name``.
        If no such instance exists, the result depends on the value of
        ``create_if_absent``. If ``create_if_absent`` is ``True``, the
        factory function specified for ``attr_name`` in
        ``_create_from_attr`` is used to return a new instance; if
        ``create_if_absent`` is ``False``, a ``KeyError`` is raised.

        If ``attr_value`` is ``None``, a ``ValueError`` is raised. If
        ``create_if_absent`` is ``True`` and no factory function is
        specified for ``attr_name`` in ``create_from_attr``, a
        ``KeyError`` is raised.
        """
        if attr_value is None:
            raise ValueError
        existing = subclass._instances[attr_name].get(attr_value)
        if existing is not None:
            return existing
        elif create_if_absent:
            create_func = subclass._create_from_attr.get(attr_name)
            if create_func is not None:
                return create_func(attr_value)
            else:
                raise KeyError
        else:
            raise KeyError

    @classmethod
    def _set_by_attr(subclass, attr_name, attr_value, instance):
        """Indicate that a value of ``attr_value`` for the attribute
        ``attr_name`` corresponds to the subclass instance
        ``instance``. If ``attr_value`` is ``None``, or there is
        already a subclass instance corresponding to the value
        ``attr_value`` for ``attr_name``, a ValueError is raised.
        """
        if attr_value is None:
            raise ValueError
        if subclass._instances[attr_name].get(attr_value) is not None:
            raise ValueError
        subclass._instances[attr_name][attr_value] = instance

    def __init__(self):
        """Use this instance's values for each attribute in
        ``_indexed_attr_names`` to index this instance. This method
        should be called after those instance values are initialized.
        """
        for attr_name in type(self)._indexed_attr_names:
            _set_by_attr(attr_name, self[attr_name], self)

