from abc import abstractmethod, ABC

class Model(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    async def create(self, obj: dict|list) -> dict|list:
        pass

    @abstractmethod
    async def update(self, obj: dict|list) -> dict|list:
        pass

    @abstractmethod
    async def delete(self, obj: dict|list) -> dict|list:
        pass

