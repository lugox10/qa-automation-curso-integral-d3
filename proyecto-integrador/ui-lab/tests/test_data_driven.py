"""Tests data-driven: datos cargados desde JSON y YAML.

Qué demuestra este archivo
--------------------------
1. Carga de JSON en tiempo de colección (parametrize + función de carga).
2. Uso de fixtures de datos (users) definidas en conftest.py.
3. Principio de separación de datos y lógica: agregar un nuevo caso de test
   es solo agregar una línea en el archivo JSON o YAML.

Diferencia entre los dos enfoques de parametrize
-------------------------------------------------
A) load_invalid_users() se llama en tiempo de colección (antes de que pytest
   inicie los navegadores). Útil cuando quieres ver los IDs de test en la
   salida sin arrancar ningún recurso pesado.

B) La variable CART_SCENARIOS se carga en tiempo de colección (como en la API).
   Así, agregar un caso al YAML automaticamente añade un test nuevo.
"""

import json
import pytest
import yaml
from pathlib import Path
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

DATA_DIR = Path(__file__).parent.parent / "data"


# ── CARGA GLOBAL DE DATOS (igual que en la API) ──────────────────────────────

def _load_yaml(nombre: str):
    """Carga un archivo YAML de la carpeta data/ (función auxiliar local)."""
    return yaml.safe_load((DATA_DIR / nombre).read_text(encoding="utf-8"))


def _load_invalid_users():
    """Lee data/users.json y devuelve una lista de pytest.param para parametrize."""
    data = json.loads((DATA_DIR / "users.json").read_text(encoding="utf-8"))
    return [
        pytest.param(
            u["username"],
            u["password"],
            u["expected_error"],
            id=u["username"] or "username_vacio",
        )
        for u in data["invalid_users"]
    ]


# ⭐ CLAVE: Cargamos los escenarios UNA SOLA VEZ al iniciar el archivo,
# igual que en el laboratorio de API.
CART_SCENARIOS = _load_yaml("products.yaml")["cart_scenarios"]


# ── Tests ───────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("username,password,expected_error", _load_invalid_users())
def test_login_invalido_desde_json(page, username, password, expected_error):
    """Cada usuario inválido del JSON debe mostrar el error correcto."""
    login = LoginPage(page)
    login.go_to().login(username, password)
    assert expected_error in login.error_message()


# ⭐ NUEVO parametrize: ahora usa la lista global CART_SCENARIOS.
# Ya no usamos 'scenario_idx', sino que recibimos 'scenario' directamente.
@pytest.mark.parametrize(
    "scenario",
    CART_SCENARIOS,
    ids=[s["description"] for s in CART_SCENARIOS]  # Nombres bonitos en la salida
)
def test_carrito_desde_yaml(authenticated_page, scenario):
    """Verifica que la burbuja del carrito refleja el número correcto de productos.

    NOTA: Ya no necesitamos el fixture 'cart_scenarios' para los datos,
    pero podemos dejarlo en conftest.py para otros usos si existe.
    """
    inventory = InventoryPage(authenticated_page)

    for item_name in scenario["items"]:
        inventory.add_to_cart(item_name)

    assert inventory.cart_count() == scenario["count"], (
        f"Escenario '{scenario['description']}': "
        f"se esperaban {scenario['count']} ítems en el carrito."
    )