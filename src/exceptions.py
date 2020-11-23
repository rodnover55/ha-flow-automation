class FlowError(Exception):
    pass


class InfoFlowError(Exception):
    pass


class AlreadyExistsError(InfoFlowError):
    pass


class UnknownFlowTypeError(FlowError):
    pass