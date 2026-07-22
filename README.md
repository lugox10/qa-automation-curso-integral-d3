# Proyecto Integrador: Diplomado en Automatización de Pruebas (QA)
# nombre del estudiante: Carlos Andres Lugo Mesa 
#nombre de la institucion: Lite Thinking

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://python.org)
[![pytest](https://img.shields.io/badge/pytest-9.1.1-brightgreen)](https://docs.pytest.org)
[![Playwright](https://img.shields.io/badge/Playwright-1.61.0-orange)](https://playwright.dev)
[![Postman](https://img.shields.io/badge/Postman-v2.1-orange)](https://postman.com)

---

## 📚 Contexto del Proyecto

Este repositorio contiene los entregables del **módulo de Desarrollo de Scripts de Prueba** del diplomado. El objetivo es demostrar la aplicación de patrones de diseño, buenas prácticas y herramientas de automatización en tres capas distintas:

1. **UI Testing** (Interfaz de Usuario) – con Playwright + pytest.
2. **API Testing** (Servicios Web) – con Postman/Newman y Python + httpx.
3. **Diseño de Pruebas** – técnicas como EP, BVA, tablas de decisión y pairwise.

El sistema bajo prueba (SUT) incluye:
- **SauceDemo** (para UI) – una tienda en línea de prueba.
- **JSONPlaceholder** (para APIs) – una API REST falsa para prototipado.

---

## 🧠 Resumen de lo que se hizo en las Sesiones 2, 3 y 4

### Sesión 2 – UI Testing: POM, Screenplay y Data-Driven

**Problema resuelto:** el código espagueti (locators repetidos, lógica de navegación mezclada con validaciones).

**Soluciones aplicadas:**

- **Page Object Model (POM)**: cada pantalla (`LoginPage`, `InventoryPage`, `CartPage`, `CheckoutPage`) encapsula sus selectores y acciones. Si la UI cambia, solo se modifica un archivo.
- **Screenplay Pattern**: el test se narra desde la perspectiva de un `Actor` que tiene habilidades (`BrowseTheWeb`) y realiza tareas (`Login`, `AddToCart`, `CompleteCheckout`). Mejora la legibilidad y separa la intención de la implementación.
- **Data-Driven Testing**: los datos de prueba (usuarios, escenarios de carrito) viven en archivos externos (`users.json`, `products.yaml`). Agregar un nuevo caso solo requiere editar el archivo, no el código.
- **Fixtures de pytest**: `authenticated_page` provee una sesión de navegador ya logueada para cada test (scope function), mientras que `users` y `products` cargan datos una sola vez (scope session).

**Entregables:**
- Page Objects: `login_page.py`, `inventory_page.py`, `cart_page.py`, `checkout_page.py`.
- Tasks de Screenplay: `login.py`, `add_to_cart.py`, `complete_checkout.py`.
- Tests en `test_login_pom.py`, `test_login_screenplay.py`, `test_data_driven.py`.

---

### Sesión 3 – API Testing con Postman + Newman

**Problema resuelto:** explorar y automatizar pruebas de API sin depender de la interfaz gráfica de Postman.

**Soluciones aplicadas:**

- **Postman** para diseñar requests, definir variables de entorno (`base_url`) y escribir scripts de prueba (JavaScript) en las pestañas *Tests* y *Pre-request*.
- **JSON Schema** para validar la estructura de las respuestas (contrato), asegurando que campos como `id`, `name`, `email` existan y sean del tipo correcto.
- **Newman** (CLI de Postman) para ejecutar las colecciones desde la terminal, permitiendo integración con CI/CD.
- **Exportación de colecciones** como archivos `.json` versionados en Git.

**Entregables:**
- Colección `RETO_S3_<nombre>` con 5 requests sobre `/users` (GET listar, GET detalle, POST, PUT, DELETE).
- Archivo `reto_s3_users.postman_collection.json` en `api-tests/postman/`.

---

### Sesión 4 – API Testing con Python (httpx + pytest)

**Problema resuelto:** pasar de pruebas exploratorias en Postman a un código mantenible, revisable y escalable en Python.

**Soluciones aplicadas:**

- **Cliente HTTP (KISS)**: `ApiClient` envuelve a `httpx.Client` y expone métodos `get`, `post`, `put`, `delete`. Configura `base_url`, `headers` y `timeout` una sola vez.
- **Fixtures de pytest** (`conftest.py`):
  - `base_url` → la URL del SUT.
  - `auth_headers` → headers de autenticación (patrón para APIs reales).
  - `api` → instancia del cliente, creada una vez (scope session) y cerrada al final.
- **Validación de contratos** con `cumple_contrato()`, que verifica presencia y tipo de campos (versión KISS de JSON Schema).
- **Data-Driven con parametrización**: los payloads se cargan desde archivos JSON/YAML (`posts_payloads.json`, `update_cases.yaml`) y se inyectan en los tests con `@pytest.mark.parametrize`.

**Entregables:**
- `tests/test_reto_users.py` con 5 tests (listar, detalle, crear, actualizar, eliminar) usando la fixture `api`.
- Bonus: `data/users_payloads.json` con 3 casos de prueba para creación parametrizada.

---

## 🧩 Paradigmas y Patrones de Diseño

### 1. Page Object Model (POM)
- **¿Qué es?** Un patrón que crea una clase por cada pantalla de la aplicación. Cada clase contiene los selectores (locators) y los métodos que representan las acciones del usuario.
- **Ventaja:** centraliza los cambios. Si un selector cambia, se modifica en un solo lugar y todos los tests se benefician.

### 2. Screenplay Pattern
- **¿Qué es?** Un patrón de diseño para pruebas de aceptación donde un `Actor` (usuario) realiza `Tasks` (acciones de negocio) utilizando `Abilities` (herramientas como un navegador o una API).
- **Ventaja:** los tests se leen como una historia en lenguaje natural. Separa el *qué* (intención) del *cómo* (implementación). Es ideal para equipos que usan BDD o Gherkin.

### 3. Data-Driven Testing (DDT)
- **¿Qué es?** Separar los datos de la lógica de los tests. Los datos se almacenan en archivos externos (JSON, YAML, CSV) y se inyectan mediante parametrización.
- **Ventaja:** agregar un nuevo escenario de prueba no requiere modificar el código, solo el archivo de datos. Reduce el riesgo de errores y facilita la colaboración con analistas funcionales.

### 4. Fixtures en pytest
- **¿Qué son?** Funciones que proporcionan un contexto o recurso a los tests (ej. un cliente HTTP, una página de navegador).
- **Scopes:** `function` (por test), `class`, `module`, `session` (una vez por toda la ejecución). Permiten optimizar el tiempo de ejecución y compartir recursos pesados.

### 5. Principios DRY y KISS
- **DRY** (*Don't Repeat Yourself*): evitar duplicación. Los locators, la configuración de la API y los datos se definen una sola vez.
- **KISS** (*Keep It Simple, Stupid*): usar la solución más simple que funcione. Por ejemplo, `ApiClient` tiene 5 métodos y cero herencia.

---

## 📁 Estructura del Proyecto
curso-main/
├── proyecto-integrador/
│ ├── ui-lab/ # Laboratorio de UI (Sesión 2)
│ │ ├── conftest.py # Fixtures compartidas
│ │ ├── pages/ # Page Objects
│ │ │ ├── login_page.py
│ │ │ ├── inventory_page.py
│ │ │ ├── cart_page.py
│ │ │ └── checkout_page.py
│ │ ├── screenplay/ # Actor, Abilities y Tasks
│ │ │ ├── actor.py
│ │ │ ├── abilities/
│ │ │ │ └── browse_web.py
│ │ │ └── tasks/
│ │ │ ├── login.py
│ │ │ ├── add_to_cart.py
│ │ │ └── complete_checkout.py
│ │ ├── data/ # Datos externos
│ │ │ ├── users.json
│ │ │ └── products.yaml
│ │ ├── tests/ # Tests de UI
│ │ │ ├── test_login_pom.py
│ │ │ ├── test_login_screenplay.py
│ │ │ └── test_data_driven.py
│ │ └── pyproject.toml # Dependencias y configuración
│ │
│ ├── api-tests/ # Laboratorio de Postman (Sesión 3)
│ │ └── postman/
│ │ ├── jsonplaceholder.postman_environment.json
│ │ ├── s3_crud_jsonplaceholder.postman_collection.json
│ │ └── reto_s3_users.postman_collection.json # Tu entrega
│ │
│ ├── api-lab/ # Laboratorio de Python + pytest (Sesión 4)
│ │ ├── client/
│ │ │ └── api_client.py # Cliente HTTP KISS
│ │ ├── conftest.py # Fixtures (api, base_url, auth_headers)
│ │ ├── data/
│ │ │ ├── posts_payloads.json
│ │ │ ├── update_cases.yaml
│ │ │ └── users_payloads.json # Bonus de la Sesión 4
│ │ ├── tests/
│ │ │ ├── test_smoke_httpx.py
│ │ │ ├── test_posts_crud.py
│ │ │ ├── test_data_driven.py
│ │ │ └── test_reto_users.py # Tu entrega de la Sesión 4
│ │ └── pyproject.toml
│ │
│ └── design-lab/ # Técnicas de diseño de pruebas
│ └── ... (EP, BVA, pairwise, tablas de decisión)
│
├── sesiones/ # Material de las sesiones
│ ├── sesion-02/
│ ├── sesion-03/
│ └── sesion-04/
│
├── .gitignore
└── README.md # Este archivo

text

---

## ⚙️ Instalación y Configuración

### Requisitos previos
- Python 3.12 o superior.
- Node.js (para Newman).
- Postman (opcional, para explorar colecciones).

### 1. Clonar el repositorio

```bash
git clone https://github.com/lugox10/qa-automation-curso-integral-d3.git
cd qa-automation-curso-integral-d3
2. Configurar el laboratorio de UI (Sesión 2)
bash
cd proyecto-integrador/ui-lab
python -m uv sync --group dev
python -m uv run playwright install chromium
python -m uv run pytest -v
3. Configurar el laboratorio de API Python (Sesión 4)
bash
cd ../api-lab
python -m uv sync --group dev
python -m uv run pytest -v
4. Ejecutar colecciones de Postman con Newman (Sesión 3)
bash
cd ../api-tests
npx --yes newman run postman/reto_s3_users.postman_collection.json -e postman/jsonplaceholder.postman_environment.json
🧪 Comandos Útiles
Comando	Descripción
uv run pytest -v	Ejecuta todos los tests del laboratorio actual.
uv run pytest tests/test_reto_users.py -v	Ejecuta solo los tests del reto de la Sesión 4.
uv run pytest --headed -v	Ejecuta los tests de UI con el navegador visible (modo headed).
npx newman run <colección> -e <environment>	Ejecuta una colección de Postman desde la terminal.
🔗 Enlaces de Interés
Playwright Documentation

pytest Documentation

HTTPX Documentation

Postman Learning Center

JSONPlaceholder (API de práctica)

SauceDemo (UI de práctica)

🙋‍♂️ Créditos
Este proyecto fue desarrollado como parte del Diplomado en Automatización de Pruebas – Módulo de Desarrollo de Scripts de Prueba.
Agradecimientos al profesor y a los compañeros del curso.

Última actualización: 22 de julio de 2026 📅
