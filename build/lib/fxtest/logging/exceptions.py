

class FxtestException(Exception):
    def __init__(self,msg=None,screen=None, stacktrace=None):
        self.msg=msg
        self.screen=screen
        self.stacktrace=stacktrace
    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.screen is not None:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg

class NotFindElementError(FxtestException):
    """
    No element errors were found
    """
    pass


class TestFixtureRunError(FxtestException):
    """
    Test fixture run error
    """
    pass


class FileTypeError(FxtestException):
    """
    Data file type error
    """
    pass
