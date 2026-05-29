"""Modèles de données liés à la boutique."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ShopItem:
    """Objet cosmétique affiché dans la boutique."""

    item_id: int
    name: str
    description: str
    price_points: int
    item_type: str


@dataclass(frozen=True)
class ShopUserState:
    """État boutique de l'utilisateur connecté."""

    points: int
    active_badge_id: Optional[int]
    active_title_id: Optional[int]
    active_theme_id: Optional[int]


@dataclass(frozen=True)
class ShopData:
    """Données nécessaires à la vue boutique."""

    user_id: Optional[int]
    catalogue: list[ShopItem]
    owned: list[int]
    points: int
    active_badge_id: Optional[int]
    active_title_id: Optional[int]
    active_theme_id: Optional[int]


@dataclass(frozen=True)
class PurchaseResult:
    """Résultat d'une tentative d'achat."""

    success: bool
    message: str


@dataclass(frozen=True)
class ActivationResult:
    """Résultat d'une tentative d'activation d'objet."""

    success: bool
    message: str
