import asyncio
import time
from typing import Dict, Callable, List, Coroutine

from tgtg import TgtgClient



class Picture:
    # picture_id: str
    # current_url: str
    # is_automatically_created: bool

    def __init__(self) -> None:
        pass

    def __init__(self, data: any) -> None:
        self.picture_id = data['picture_id']
        self.current_url = data['current_url']
        self.is_automatically_created = data['is_automatically_created']


class Location:
    longitude: float
    latitude: float
    country: str
    address_line: str
    city: str
    postal_code: str

    def __init__(self) -> None:
        pass

    def __init__(self, data: any) -> None:
        self.longitude = data['location']['longitude']
        self.latitude = data['location']['latitude']
        self.country = data['address']['country']['name']
        self.address_line = data['address']['address_line']
        self.city = data['address']['city']
        self.postal_code = data['address']['postal_code']


class Store:
    store_id: str
    store_name: str
    branch: str
    description: str
    tax_identifier: str
    website: str
    store_location: Location
    logo_picture: Picture
    store_time_zone: str
    hidden: bool
    favorite_count: int
    we_care: bool
    distance: float
    cover_picture: Picture
    uses_ecommerce_model: bool

    def __init__(self) -> None:
        pass

    def __init__(self, data: any) -> None:
        self.store_id = data['store_id']
        self.store_name = data['store_name']
        self.branch = data.get('branch', '')
        self.description = data['description']
        self.tax_identifier = data['tax_identifier']
        self.website = data['website']
        self.store_location = Location(data['store_location'])
        self.logo_picture = Picture(data['logo_picture'])
        self.store_time_zone = data['store_time_zone']
        self.hidden = data['hidden']
        self.favorite_count = data['favorite_count']
        self.we_care = data['we_care']
        self.distance = data['distance']
        self.cover_picture = Picture(data['cover_picture'])
        self.uses_ecommerce_model = data['uses_ecommerce_model']

# TODO add price and rating
class Item:
    item_id: str
    name: str
    favorite_count: int
    store: Store
    display_name: str
    pickup_location: Location
    items_available: int
    distance: float
    favorite: bool
    in_sales_window: bool
    new_item: bool

    def __init__(self) -> None:
        pass

    def __init__(self, data:any) -> None:
        self.item_id = data['item']['item_id']
        self.name = data['item']['name']
        self.favorite_count = data['item']['favorite_count']
        self.store = Store(data['store'])
        self.display_name = data['display_name']
        self.pickup_location = data['pickup_location']
        self.items_available = data['items_available']
        self.distance = data['distance']
        self.favorite = data['favorite']
        self.in_sales_window = data['in_sales_window']
        self.new_item = data['new_item']

class TGTGManager:
    _data: Dict[str, Item]
    _handler: Callable[[Item], Coroutine]

    def __init__(self, access_token:str, refresh_token:str, user_id:str):
        self._client = TgtgClient(access_token=access_token, refresh_token=refresh_token, user_id=user_id)
        self._data = dict()
        self._handler = lambda item : Coroutine()

    def on_new(self, handler: Callable[[Item], Coroutine]):
        self._handler = handler

    async def _handle_new_items(self, items:List[Item]):
        for item in items:
            if item.item_id not in self._data:
                await self._handler(item)
        self._data = dict([(item.item_id, item) for item in items])

    async def watch(self, latitude:float, longitude:float, radius:float, interval:float):
        def get_items():
            return [Item(data) for data in
                     self._client.get_items(latitude=latitude, longitude=longitude, radius=radius, favorites_only=False,
                                      with_stock_only=True)]
        while True:
            items = get_items()
            await self._handle_new_items(items)
            await asyncio.sleep(interval)
