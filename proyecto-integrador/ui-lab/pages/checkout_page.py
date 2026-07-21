"""Page Object de la pantalla de checkout (Step One) de SauceDemo."""

from __future__ import annotations
from playwright.sync_api import Page


class CheckoutPage:
    """Representa https://www.saucedemo.com/checkout-step-one.html."""

    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        self.page = page
        self._first_name   = page.locator('[data-test="firstName"]')
        self._last_name    = page.locator('[data-test="lastName"]')
        self._postal_code  = page.locator('[data-test="postalCode"]')
        self._continue_btn = page.locator('[data-test="continue"]')
        self._error_msg    = page.locator('[data-test="error"]')

    # ── Acciones ──────────────────────────────────────────────────────────

    def fill_shipping(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutPage":
        """Rellena los campos de información de envío y devuelve self (fluent)."""
        self._first_name.fill(first_name)
        self._last_name.fill(last_name)
        self._postal_code.fill(postal_code)
        return self

    def continue_to_overview(self) -> None:
        """Hace clic en el botón 'Continue' para ir a la vista de resumen."""
        self._continue_btn.click()

    # ── Consultas ─────────────────────────────────────────────────────────

    def has_error(self) -> bool:
        """True si hay un mensaje de error visible en la pantalla."""
        return self._error_msg.is_visible()

    def error_message(self) -> str:
        """Texto del mensaje de error (para validaciones más detalladas)."""
        return self._error_msg.inner_text()