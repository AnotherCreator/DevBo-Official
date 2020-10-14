class MyError(Exception):
    class Error(Exception):
        pass

    class ValueTooLargeError(Exception):
        pass

    class ValueTooSmallError(Exception):
        pass

    class InvalidValue(Exception):
        pass

    class MissingRequiredArgument(Exception):
        pass
