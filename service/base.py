from abc import ABC, abstractmethod


class Repository(ABC):
    
    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplemented
    
    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplemented
    
    # @abstractmethod
    # async def get_multi(self, *args, **kwargs):
    #     raise NotImplemented
    
    # @abstractmethod
    # async def upgrade(self, *args, **kwargs):
    #     raise NotImplemented
    
    # @abstractmethod
    # async def delete(self, *args, **kwargs):
    #     raise NotImplemented