from esengine.utils.payload.meta_util import (
    make_struct, unroll_definitions, unroll_struct
)


class MetaFilterQuery(type):
    def __init__(self, name, bases, d):
        super(MetaFilterQuery, self).__init__(name, bases, d)
        unroll_definitions(self._definitions)

    def __getattr__(self, key):
        if key == '__test__':
            return None

        self._validate_key(key)
        return lambda *args, **kwargs: self(
            key,
            make_struct(self._definitions[key], *args, **kwargs)
        )

    def _validate_key(self, key):
        if key != "__slots__" and key not in self._definitions:
            raise self._exception(key)


class MetaAggregate(MetaFilterQuery):
    def __getattr__(self, key):
        if key == '__test__':
            return None

        self._validate_key(key)
        return lambda *args, **kwargs: self(
            key,
            args[0],
            make_struct(self._definitions[key], *args[1:], **kwargs)
        )


class MetaSuggester(MetaFilterQuery):
    def __getattr__(self, key):
        if key == '__test__':
            return None

        self._validate_key(key)
        return lambda *args, **kwargs: self(
            key,
            args[0],
            args[1],
            make_struct(self._definitions[key], *args[2:], **kwargs)
        )


class BaseFilterQuery(object):
    _struct = None
    _dsl_type = None

    def __init__(self, dsl_type, struct):
        self._dsl_type = dsl_type
        self._struct = struct

    @property
    def dict(self):
        return self.as_dict()

    def as_dict(self):
        # Handle reserved Python keyword alternatives (from_, or_)
        dsl_type = (
            self._dsl_type[:-1]
            if self._dsl_type.endswith('_')
            else self._dsl_type
        )
        return {dsl_type: unroll_struct(self._struct)}


class BaseAggregate(BaseFilterQuery):
    _name = None

    def __init__(self, dsl_type, name, struct):
        self._dsl_type = dsl_type
        self._struct = struct
        self._name = name
        self._aggs = []

    def as_dict(self):
        struct = {
            self._name: {
                self._dsl_type: unroll_struct(self._struct)
            }
        }

        if self._aggs:
            aggregates = {}

            for agg in self._aggs:
                aggregates.update(agg.as_dict())

            struct[self._name]['aggregations'] = aggregates

        return struct

    def aggregate(self, *aggregates):
        self._aggs.extend(aggregates)
        return self


class BaseSuggester(BaseFilterQuery):
    _name = None

    def __init__(self, dsl_type, name, text, struct):
        self._dsl_type = dsl_type
        self._struct = struct
        self._name = name
        self._text = text
        self._suggs = []

    def as_dict(self):
        struct = {
            self._name: {
                "text": self._text,
                self._dsl_type: unroll_struct(self._struct)
            }
        }

        if self._suggs:
            for sugg in self._suggs:
                struct.update(sugg.as_dict())

        return struct
