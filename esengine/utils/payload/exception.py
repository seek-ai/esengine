

class ElasticQueryException(Exception):
    pass


class DslException(ElasticQueryException):
    pass


class NoQuery(DslException):
    pass


class NoFilter(DslException):
    pass


class NoAggregate(DslException):
    pass


class NoSuggester(DslException):
    pass


class InvalidArg(DslException):
    pass


class MissingArg(DslException):
    pass
