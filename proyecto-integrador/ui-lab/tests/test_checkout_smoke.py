import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from screenplay.actor import Actor
from screenplay.abilities.browse_web import BrowseTheWeb
from screenplay.tasks.complete_checkout import CompleteCheckout


def test_checkout_page_has_error_sin_datos(authenticated_page):
    # Agregar un producto al carrito para poder ir al checkout
    InventoryPage(authenticated_page).add_to_cart("Sauce Labs Backpack").go_to_cart()
    CartPage(authenticated_page).proceed_to_checkout()

    checkout = CheckoutPage(authenticated_page)
    # No llenar datos, hacer clic en continue
    checkout.continue_to_overview()
    assert checkout.has_error(), "Debería mostrar error por falta de datos"
    assert "Error: First Name is required" in checkout.error_message()


def test_complete_checkout_task(authenticated_page):
    actor = Actor("Tester").can(BrowseTheWeb.using(authenticated_page))
    actor.attempts_to(
        CompleteCheckout.with_info("Juan", "Pérez", "12345")
    )
    # Después de continuar, debería estar en la página de overview
    # (esto lo validamos con la URL)
    assert authenticated_page.url == "https://www.saucedemo.com/checkout-step-two.html"