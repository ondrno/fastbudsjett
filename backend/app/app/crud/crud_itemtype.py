from app.crud.base import CRUDBase
from app.schemas.itemtype import ItemType, ItemTypeCreate, ItemTypeUpdate


class CRUDItemType(CRUDBase[ItemType, ItemTypeCreate, ItemTypeUpdate]):
    pass


itemtype = CRUDItemType(ItemType)
