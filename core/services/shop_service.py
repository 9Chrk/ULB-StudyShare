"""Services métier liés à la boutique."""

from core.db.manager import DBManager
from core.repository.shop_repository import get_catalogue, get_owned_item_ids


def get_shop_data(user_id):
    """Renvoie le catalogue et les objets possédés."""
    with DBManager() as cursor:
        catalogue = get_catalogue(cursor)
        owned = get_owned_item_ids(cursor, user_id) if user_id else []
        return {"catalogue": catalogue, "owned": owned}
