from dataclasses import dataclass

@dataclass
class BaseTaskRepository:
    def get_all(self):
        raise NotImplementedError
    
    def get_one_or_none(self, **filter_by):
        raise NotImplementedError
    
    def add(self, data):
        raise NotImplementedError
    
    def edit(self, data, exclude_unset: bool = False, **filter_by):
        raise NotImplementedError
    
    def delete(self, **filter_by):
        raise NotImplementedError
