# 🛒 E-Commerce Test Automation Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/selenium-4.15.0-green)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-7.4.3-orange)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

A professional test automation framework for e-commerce web applications using Python, Selenium WebDriver, and PyTest with Page Object Model.

## 🎯 Features

- ✅ **Page Object Model** - Clean, maintainable, and reusable code structure
- ✅ **Data-Driven Testing** - Test multiple scenarios with JSON data files
- ✅ **Automatic Screenshots** - Captures screenshots on test failures
- ✅ **HTML Reports** - Professional, self-contained test reports
- ✅ **Detailed Logging** - Comprehensive execution logs
- ✅ **Parallel Execution** - Faster test execution with pytest-xdist
- ✅ **Cross-Browser Support** - Easily extendable to multiple browsers

## 🏗️ Project Structure
Ecommerce-Test-Automation/
├── tests/ # Test cases
│ ├── test_login.py
│ ├── test_cart.py
│ └── test_checkout.py
├── pages/ # Page Object classes
│ ├── base_page.py
│ ├── login_page.py
│ ├── inventory_page.py
│ ├── cart_page.py
│ └── checkout_page.py
├── utils/ # Utility modules
│ ├── driver_factory.py
│ ├── logger.py
│ ├── screenshot.py
│ └── helpers.py
├── testdata/ # Test data files
│ └── users.json
├── reports/ # Test reports (generated)
├── screenshots/ # Screenshots on failure (generated)
├── conftest.py # PyTest configuration
├── pytest.ini # PyTest settings
├── run_tests.py # Test execution script
└── requirements.txt

text

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Git (optional, for cloning)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/Ecommerce-Test-Automation.git
cd Ecommerce-Test-Automation
Create and activate virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Running Tests
bash
# Run all tests
python run_tests.py

# Run specific test file
pytest tests/test_login.py -v

# Run smoke tests only
pytest -m smoke -v

# Run with HTML report
pytest --html=reports/report.html --self-contained-html
📊 Test Results
After running tests, you'll find:

HTML Report: reports/test_report.html

Logs: reports/test_execution.log

Screenshots: screenshots/ (on failures only)

🧪 Test Scenarios
Login Tests
✅ Valid login with correct credentials

✅ Invalid login with wrong credentials

✅ Locked out user handling

✅ Empty credentials validation

✅ Missing username/password validation

Cart Tests
✅ Add single item to cart

✅ Add multiple items to cart

✅ Remove items from cart

✅ Cart persistence across navigation

Checkout Tests
✅ Complete checkout process

✅ Empty cart checkout

✅ Missing information validation

🛠️ Technologies Used
Technology	Version	Purpose
Python	3.8+	Programming language
Selenium	4.15.0	Web automation
PyTest	7.4.3	Test framework
Pytest-HTML	4.1.1	HTML reporting
Pytest-XDist	3.5.0	Parallel execution
Faker	20.1.0	Test data generation
OpenPyXL	3.1.2	Excel file support
📝 Resume Description
E-Commerce Test Automation Framework | Python, Selenium, PyTest

Designed a modular UI automation framework using the Page Object Model for an e-commerce web application

Automated login, cart, and checkout workflows with positive and negative test cases

Implemented data-driven testing using JSON, HTML reporting, logging, and automatic screenshot capture on failures

Structured the project for maintainability with reusable page classes and utility modules

Achieved 100% pass rate on critical test scenarios

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
SauceDemo - Test website

Selenium - Web automation framework

PyTest - Testing framework