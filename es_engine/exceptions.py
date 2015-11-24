class ClientError(Exception):
    pass


class RequiredField(Exception):
    pass


class InvalidMultiField(Exception):
    pass


class FieldTypeMismatch(Exception):

    def __init__(self, field_name, expected_type, actual_type):
        message = "`{}` expected `{}`, actual `{}`".format(
            field_name, expected_type, actual_type)
        Exception.__init__(self, message)
