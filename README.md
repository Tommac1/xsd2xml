# 💡 xsd2xml 💡

![Build Status](https://github.com/Tommac1/xsd2xml/actions/workflows/github-actions.yml/badge.svg?branch=dev)
[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/Status-Wheel%20Package%20Available-yellow.svg)](https://pypi.org/)

**xsd2xml** is a simple Python tool that converts an XSD schema file into a structured XML file.
Built for developers who need to generate XML files quickly from existing schemas, it automates the process
and reduces manual work.

---

## 💎 Features

- Generate XML files from XSD schema files
- Lightweight and easy to use, uses only `xmlschema` and `xml.etree`
- Available as a local wheel package for now
- Python 3.10+ compatible
- Future support for PyPI upload

## 🚧 TODO

- Add more docstring to the project
- pylint compliance
- Add release workflow
- Implement more tests

---

## 🛠️ Installation

At the moment, **xsd2xml** is available only as a locally-built wheel package. Here's how you can install it:

1. Clone the repository:
    ```bash
    git clone https://github.com/Tommac1/xsd2xml.git
    ```

2. Navigate to the project directory:
    ```bash
    cd xsd2xml
    ```

3. Build the wheel package:
    ```bash
    pip install -r requirements.txt
    python -m build
    ```

4. Install the package locally:
    ```bash
    pip install dist/*.whl
    ```

---

## 🚀 Usage

You can generate an XML file from an XSD schema using the command line:

```bash
xsd2xml xsd_path xml_path
```

Or you can use it in your source code:

```python
from xsd2xml import xsd2xml

xml_gen = xsd2xml.Xsd2Xml('my_schema.xsd')
xml_gen.gen_xml()
xml_gen.save_xml('my_output.xml')
```

---

## 🧪 Run tests

To run tests, simply type in root directory:
```bash
pytest
```

---

## 🤝 Contributing

We welcome contributions to **xsd2xml**! To keep the codebase clean and maintainable, we ask all contributors to follow a few guidelines before submitting their pull requests:

### 📝 Guidelines

1. **PEP8 Compliance** 🐍:
   - All code must adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/), the Python style guide.
   - You can check your code using:
     ```bash
     flake8 your_module.py
     ```

2. **Unit Tests** ✅:
   - Ensure your changes are fully covered by tests.
   - Run all tests to make sure nothing breaks:
     ```bash
     pytest
     ```

3. **Pre-Commit Hooks** 🔧:
   - We use [pre-commit](https://pre-commit.com/) to automatically check code formatting and linting before committing. Make sure you install the hooks locally:
     ```bash
     pre-commit install
     ```
   - Run the pre-commit checks manually before committing:
     ```bash
     pre-commit run --all-files
     ```

### 🧪 Submitting a Pull Request

1. Fork the repository and create your feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```

2. Make sure your code passes all checks (PEP8, unit tests, pre-commit hooks).

3. Submit a pull request with a detailed description of your changes.

### 💵 Donations

For donations, we encourage you to support a local charity or animal shelter.
Your help can make a difference in someone's life or provide care for animals in need. ❤️

If you would still like to contribute to the project in some other way, feel free to reach out or let us know.
We’re always happy to hear from you!

---

Thank you for using xsd2xml! We hope it simplifies your XML generation process.
