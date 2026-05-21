"""Thème partagé pour les vues Tkinter de l'application."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ColorPalette:
    # Neutrals
    white: str = "#ffffff"
    black: str = "#000000"
    # Gray
    gray_50: str = "#f3f4f6"
    gray_200: str = "#e5e7eb"
    gray_400: str = "#9CA3AF"
    gray_500: str = "#A1A1A1"
    gray_600: str = "#6b7280"
    gray_700: str = "#374151"
    gray_800: str = "#333333"
    gray_900: str = "#111827"
    # Blue
    blue_400: str = "#3b82f6"
    blue_600: str = "#2563eb"
    # Navy
    navy_800: str = "#2A2A45"
    navy_900: str = "#1B1B33"
    navy_950: str = "#141429"
    # Teal
    teal_300: str = "#1DE9B6"
    # Emerald
    emerald_100: str = "#dcfce7"
    emerald_300: str = "#d1fae5"
    emerald_500: str = "#10b981"
    emerald_600: str = "#059669"
    emerald_800: str = "#166534"
    # Amber
    amber_400: str = "#f59e0b"
    # Red
    red_500: str = "#ef4444"
    red_900: str = "#5B100F"

COLORS = ColorPalette()

WORKSPACE_BACKGROUND = COLORS.gray_50
WORKSPACE_SURFACE = COLORS.white
WORKSPACE_TEXT = COLORS.gray_900
WORKSPACE_MUTED = COLORS.gray_600
WORKSPACE_BORDER = COLORS.gray_200
WORKSPACE_BLUE_LIGHT = COLORS.blue_400
WORKSPACE_BLUE_DARK = COLORS.blue_600
WORKSPACE_GREEN = COLORS.emerald_500
WORKSPACE_GREEN_DARK = COLORS.emerald_600
WORKSPACE_GREEN_LIGHT = COLORS.emerald_100
WORKSPACE_GREEN_TEXT = COLORS.emerald_800
WORKSPACE_HIGHLIGHT = COLORS.emerald_300
WORKSPACE_NEUTRAL_TEXT = COLORS.gray_700
WORKSPACE_ORANGE = COLORS.amber_400
WORKSPACE_RED = COLORS.red_500

SIDEBAR_BACKGROUND = COLORS.navy_950
SIDEBAR_ACTIVE_TEXT = COLORS.teal_300
SIDEBAR_INACTIVE_TEXT = COLORS.white
SIDEBAR_ACTIVE_BACKGROUND = COLORS.navy_900
SIDEBAR_SEPARATOR = COLORS.navy_800
SIDEBAR_EXIT_SEPARATOR = COLORS.gray_800
SIDEBAR_EXIT_BACKGROUND = COLORS.red_900
SIDEBAR_ICON_INACTIVE = COLORS.gray_400
