"""Task: CompleteCheckout — realiza el flujo completo de checkout."""

from __future__ import annotations
from screenplay.abilities.browse_web import BrowseTheWeb
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class CompleteCheckout:
    """Tarea de alto nivel: llenar datos de envío y continuar al resumen."""

    def __init__(self, first_name: str, last_name: str, postal_code: str) -> None:
        self._first_name = first_name
        self._last_name = last_name
        self._postal_code = postal_code

    @classmethod
    def with_info(cls, first_name: str, last_name: str, postal_code: str) -> "CompleteCheckout":
        """Constructor expresivo: CompleteCheckout.with_info('Juan', 'Pérez', '12345')."""
        return cls(first_name, last_name, postal_code)

    def perform_as(self, actor) -> None:
        page = actor.ability_to(BrowseTheWeb).page

        # Ir al carrito
        InventoryPage(page).go_to_cart()
        # Ir a checkout
        CartPage(page).proceed_to_checkout()
        # Rellenar datos y continuar
        CheckoutPage(page).fill_shipping(
            self._first_name,
            self._last_name,
            self._postal_code
        ).continue_to_overview()