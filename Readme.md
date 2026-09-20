# E-Commerce Test Automation (Selenium + Pytest)

![Tests](https://github.com/<your-username>/Ecommerce-Test-Automation/actions/workflows/tests.yml/badge.svg)

UI test automation framework for the [Swag Labs](https://www.saucedemo.com/) demo store, built with **Python, Selenium WebDriver and Pytest** using the **Page Object Model**.

## Features

- **Page Object Model**: locators and page actions live in page classes; tests contain only test logic and assertions
- **Pytest fixtures and markers**: `smoke`, `regression` and `critical` markers for selective runs
- **Self-contained HTML report** with a **screenshot embedded automatically on every failure**
- **Centralised logging** of every navigation, click and input
- **Externalised test data** (JSON) for users and checkout details
- **Headless mode** controlled by an environment variable, so the same code runs locally and in CI
- **CI** with GitHub Actions: the suite runs on every push and the report is uploaded as an artifact

## Tech stack

Python 3.12, Selenium 4, Pytest, pytest-html, pytest-xdist, Faker, GitHub Actions

## Test coverage (12 tests)

| Area | Scenarios |
|---|---|
| **Login** | valid login, invalid login, locked-out user, empty credentials, username only |
| **Cart** | add one item, add multiple items, remove item, cart persistence across navigation |
| **Checkout** | complete checkout, checkout with an empty cart, checkout with missing information |

## Project structure

```
Ecommerce-Test-Automation/
├── .github/workflows/tests.yml   # CI pipeline
├── pages/                        # Page Objects (base, login, inventory, cart, checkout)
├── tests/                        # test_login.py, test_cart.py, test_checkout.py
├── utils/                        # driver factory, logger, screenshots, helpers
├── conftest.py                   # fixtures, failure screenshots, report hooks
├── pytest.ini                    # default options and report settings
└── requirements.txt
```

## Getting started

```bash
git clone https://github.com/<your-username>/Ecommerce-Test-Automation.git
cd Ecommerce-Test-Automation

python -m venv venv
# Windows:  venv\Scripts\activate
# macOS/Linux:  source venv/bin/activate

pip install -r requirements.txt
```

Chrome must be installed. Selenium 4 downloads the matching driver automatically.

## Running the tests

```bash
pytest                      # run everything
pytest -m smoke             # smoke tests only
pytest -m critical          # critical-path tests only
pytest tests/test_login.py  # a single file
pytest -n 3                 # run in parallel (pytest-xdist)
```

Run headless (no visible browser):

```bash
# Windows PowerShell
$env:HEADLESS="1"; pytest

# macOS/Linux
HEADLESS=1 pytest
```

## Reports

After each run, open `reports/report.html`. Failed tests include a screenshot of the browser at the moment of failure (also saved in `screenshots/`).

## Continuous integration

`.github/workflows/tests.yml` installs dependencies, runs the suite on every push and pull request, and uploads the HTML report and screenshots as a downloadable artifact.