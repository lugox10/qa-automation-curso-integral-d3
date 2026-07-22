"""Reto Sesión 4: refactorización de la suite CRUD de /users a Python.

Requisitos:
- 5 tests mínimos (listar, detalle, crear, actualizar, eliminar).
- Todos usan la fixture `api` (no se escribe la URL completa).
- Contrato validado con `cumple_contrato`.
- Datos de creación desde JSON (bonus).
"""

import time
import pytest
from conftest import load_json

# ── Contrato del recurso user (igual que en Postman) ──────────────────────
CONTRATO_USER = {
    "id": int,
    "name": str,
    "username": str,
    "email": str,
    # Nota: JSONPlaceholder también devuelve "address", "phone", "website",
    # pero no son obligatorios para el contrato mínimo.
}


def cumple_contrato(recurso: dict, contrato: dict) -> bool:
    """Valida presencia y tipo de cada campo."""
    return all(
        campo in recurso and isinstance(recurso[campo], tipo)
        for campo, tipo in contrato.items()
    )


# ── Tests ──────────────────────────────────────────────────────────────────

def test_listar_users_devuelve_10(api):
    """GET /users → 200, 10 usuarios."""
    respuesta = api.get("/users")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert isinstance(datos, list)
    assert len(datos) == 10


def test_detalle_user_cumple_contrato(api):
    """GET /users/1 → 200, contrato válido."""
    respuesta = api.get("/users/1")
    assert respuesta.status_code == 200
    user = respuesta.json()
    assert cumple_contrato(user, CONTRATO_USER)


def test_crear_user_devuelve_201_y_eco(api):
    """POST /users → 201, el nombre generado coincide."""
    nombre_unico = f"Usuario QA {time.time_ns()}"
    payload = {
        "name": nombre_unico,
        "username": "qa_user",
        "email": "qa@example.com",
        # JSONPlaceholder no requiere más campos para crear
    }
    respuesta = api.post("/users", json=payload)
    assert respuesta.status_code == 201
    creado = respuesta.json()
    assert creado["name"] == nombre_unico
    # Además, debe tener un id asignado
    assert isinstance(creado.get("id"), int)


def test_actualizar_user_devuelve_200_y_campo_actualizado(api):
    """PUT /users/1 → 200, el campo actualizado coincide."""
    payload = {
        "id": 1,
        "name": "Usuario Actualizado",
        "username": "updated_user",
        "email": "updated@example.com",
    }
    respuesta = api.put("/users/1", json=payload)
    assert respuesta.status_code == 200
    actualizado = respuesta.json()
    assert actualizado["name"] == payload["name"]
    assert actualizado["username"] == payload["username"]


def test_eliminar_user_devuelve_200_y_body_vacio(api):
    """DELETE /users/1 → 200, body vacío {}."""
    respuesta = api.delete("/users/1")
    assert respuesta.status_code == 200
    assert respuesta.json() == {}


# ── Bonus: data-driven con JSON ──────────────────────────────────────────

@pytest.mark.parametrize(
    "caso",
    load_json("users_payloads.json"),
    ids=[c["caso"] for c in load_json("users_payloads.json")]
)
def test_crear_user_desde_json(api, caso):
    respuesta = api.post("/users", json=caso["payload"])
    assert respuesta.status_code == 201
    creado = respuesta.json()
    for campo, valor in caso["payload"].items():
        assert creado[campo] == valor