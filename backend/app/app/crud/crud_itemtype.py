from app.crud.base import CRUDBase
from app.models.itemtype import ItemType
from app.schemas.itemtype import ItemTypeCreate, ItemTypeUpdate


class CRUDItemType(CRUDBase[ItemType, ItemTypeCreate, ItemTypeUpdate]):
    pass


itemtype = CRUDItemType(ItemType)
