from dataclasses import dataclass


@dataclass
class ModelObject:
    id: int

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

    @property
    def fields(self):
        return tuple(self.__dict__.keys())

    @property
    def values(self):
        return tuple(self.__dict__.values())

    def structure(self):
        return tuple(self.__dict__.items())
