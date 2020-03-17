import uuid
import re
from typing import Dict
from dataclasses import dataclass, field
from models.model import Model


@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False, default="stores")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return{
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    # find a store in the database  matching the name passed in and return it
    def get_by_name(cls, store_name: str) -> "Store": # Store.get_by_name('John Lewis')
        return cls.find_one_by("name", store_name)

    @classmethod
    # use the url prefix that we pass in and find a store that has that
    def get_by_url_prefix(cls, url_prefix: str)  -> "Store":
        # find the urls that start with the url prefix -- does not need to match exactly, only start with it
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        """
        Return a store from a url like "https://www.johnlewis.com/item/sdfj4h5g4g21k.html"
        :param url: The item's URL
        :return: a Store
        """
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)