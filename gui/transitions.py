"""Helpers pour les transitions visuelles (alpha, effets, etc.)."""

import tkinter as tk
from typing import Callable, Optional
from time import sleep


def with_alpha_transition(
    root: tk.Tk, callback: Callable, hidden_alpha: float = 0.0
) -> None:
    """Exécute callback en rendant la fenêtre temporairement transparente."""

    original_alpha = _get_window_alpha(root)

    # Si l'alpha n'est pas supporté, on exécute simplement le callback sans transition.
    if original_alpha is None:
        callback()
        return

    # Essayer de rendre la fenêtre transparente avant d'exécuter le callback.
    if not _set_window_alpha(root, hidden_alpha):
        callback()
        return

    # Exécuter le callback pendant que la fenêtre est transparente.
    callback()
    root.update_idletasks()

    sleep(0.2)
    _set_window_alpha(root, original_alpha)


# --------------------------------------------------------
# Méthodes utilitaires internes
# --------------------------------------------------------


def _get_window_alpha(root: tk.Tk) -> Optional[float]:
    """Retourne l'alpha courant, ou None si non supporté."""
    try:
        return float(root.attributes("-alpha"))
    except tk.TclError:
        return None


def _set_window_alpha(root: tk.Tk, value: float) -> bool:
    """Essaie de changer l'alpha, renvoie True si OK, False sinon."""
    if value is None:
        return False

    try:
        root.attributes("-alpha", value)
        return True
    except tk.TclError:
        return False
