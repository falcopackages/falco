# Falco

**An opinionated toolkit for building web apps faster with Django**

<img align="right" width="170" height="150" src="https://raw.githubusercontent.com/Tobi-De/falco/main/docs/_static/falco-logo.svg">

[![CI](https://github.com/Tobi-De/falco/actions/workflows/ci.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/ci.yml)
[![Publish Python Package](https://github.com/Tobi-De/falco/actions/workflows/publish.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/publish.yml)
[![Documentation](https://readthedocs.org/projects/falco-cli/badge/?version=latest&style=flat)](https://beta.readthedocs.org/projects/falco-cli/builds/?version=latest)
[![pypi](https://badge.fury.io/py/falco-cli.svg)](https://pypi.org/project/falco-cli/)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Tobi-De/falco/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/falco-cli)](https://pypi.org/project/falco-cli/)
[![PyPI - Versions from Framework Classifiers](https://img.shields.io/pypi/frameworkversions/django/falco-cli)](https://pypi.org/project/falco-cli/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/falco-cli)](https://pypistats.org/packages/falco-cli)

Falco is an opinionated toolkit designed to speed up web app development with Django. It helps you get to production in just a few hours while keeping your project close to the standard Django structure, keeping things simple and manageable.


## 🚀 Features

- Django 5.1 and Python 3.11 support
- Email Login via [django-allauth](https://django-allauth.readthedocs.io/en/latest/)
- [CRUD View Generation](https://falco.oluwatobi.dev/the_cli/crud.html) for your models with optional integrations with `django-tables2` and `django-filters`.
- Built-in **Project Versioning** with `bump2version`, Git integration, automatic changelog updates, and GitHub release creation.
- **Automated Deployment**: Deploy your project to a VPS (using [fabric](https://www.fabfile.org/)) or Docker-based platform with ease.
- Styling with [Tailwind CSS](https://tailwindcss.com/) (including [DaisyUI](https://daisyui.com/)) or [Bootstrap](https://getbootstrap.com/).
- And much more! Check out the full list of packages [here](https://falco.oluwatobi.dev/the_cli/start_project/packages.html)


## Table of Contents

- [Falco](#falco)
  - [🚀 Features](#-features)
  - [Table of Contents](#table-of-contents)
  - [📖 Installation](#-installation)
  - [♥️ Acknowledgements](#️-acknowledgements)
  - [License](#license)

## 📖 Installation

```console
pip install falco-cli
```

Read the [documentation](https://falco.oluwatobi.dev) for more information on how to use Falco.

## ♥️ Acknowledgements

Falco is inspired by (and borrows elements from) some excellent open source projects:

- [django-twc-project](https://github.com/westerveltco/django-twc-project)
- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [fuzzy-couscous](https://github.com/Tobi-De/fuzzy-couscous) (predecessor of falco)
- [django-hatch-startproject](https://github.com/oliverandrich/django-hatch-startproject)
- [django-unicorn](https://github.com/adamghill/django-unicorn) (Inspiration for the logo)
- [neapolitan](https://github.com/carltongibson/neapolitan)
- [django-base-site](https://github.com/epicserve/django-base-site)
- [django-cptemplate](https://github.com/softwarecrafts/django-cptemplate)
- [djangox](https://github.com/wsvincent/djangox)

## License

`falco` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
