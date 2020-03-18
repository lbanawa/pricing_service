from typing import Dict
import re
import requests
import uuid
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from models.model import Model


# 'Model' passed into this method means to use the json method in 'Model' if 'Item' does not have one
@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        # have beautifulsoup read the html content
        soup = BeautifulSoup(content, "html.parser")
        # find the specific element that matches our search
        element = soup.find(self.tag_name, self.query)
        # find the price that is contained within that element -- remove any white space with .strip()
        string_price = element.text.strip()

        # r-string (aka raw string) allows us to define a string that uses regular expression syntax (aka re)
        # tell the program that the price is in a certain format using re syntax -- '\d' indicates a number
        # the brackets indicate that we are only referring to the part of the string that has that format
        # '?' means that the comma isn't necessary if for example we get a price of 500.00, or 1000.00
        pattern = re.compile(r"(\d+,?\d*\.\d\d)")
        # find if there are any matches in our string
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_commas = found_price.replace(",", "")
        self.price = float(without_commas)
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }
