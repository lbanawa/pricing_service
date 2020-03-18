from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Type, Dict, Union

from common.database import Database

# bound means T must be a Model or one of its subclasses -- it cannot be anything else
T = TypeVar('T', bound='Model')

class Model(metaclass=ABCMeta):
    # the four lines of code below are to prevent unnecessary warnings. They do not do anything.
    collection: str
    _id: str
    def __init__(self, *args, **kwargs):
        pass

    # Upsert -- Given a query, update items matching that query. If none match, then insert a new one instead.
    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by("_id", _id)

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    # this creates a cursor which is similar to a list of python dictionaries
    # displays all info present in the collection
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    # return a single element with the attribute and value specified
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T: # Example: Item.find_one_by('url', 'https://bla.com')
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    # return a list of objects
    def find_many_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> List[T]:
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]
