class Flow:
    def __init__(self, data, key):
        self.__data = data
        self.__key = key

    def id(self) -> str:
        return self.__data["flow_id"]

    def validate_step(self, step) -> bool:
        return True

    def key(self) -> str:
        return self.__key