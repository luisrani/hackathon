from abc import ABC, abstractmethod


class Service(ABC):
    URL: str

    @classmethod
    @abstractmethod
    def services(cls) -> dict[str, bool]:
        pass
