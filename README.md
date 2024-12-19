# Falco

> [!IMPORTANT]
> Work in progress, not ready, not released yet, currently this is the place to go https://github.com/falcopackages/falco-cli

**An opinionated toolkit for a better Django developer experience**

<img align="right" width="170" height="150" src="https://raw.githubusercontent.com/falcopackages/falco/refs/heads/main/docs/_static/falco-logo.svg">

[![CI](https://github.com/Tobi-De/falco/actions/workflows/ci.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/ci.yml)
[![Publish Python Package](https://github.com/Tobi-De/falco/actions/workflows/publish.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/publish.yml)
[![Documentation](https://readthedocs.org/projects/falco-app/badge/?version=latest&style=flat)](https://beta.readthedocs.org/projects/falco-app/builds/?version=latest)
[![pypi](https://badge.fury.io/py/falco-app.svg)](https://pypi.org/project/falco-app/)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Tobi-De/falco/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/falco-app)](https://pypi.org/project/falco-app/)
[![PyPI - Versions from Framework Classifiers](https://img.shields.io/pypi/frameworkversions/django/falco-app)](https://pypi.org/project/falco-app/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/falco-app)](https://pypistats.org/packages/falco-app)

Falco is an opinionated toolkit designed to speed up web app development with Django. It helps you get to production in just a few minutes while keeping your project close to the standard Django structure, keeping things simple and manageable.


## 🚀 Features

- Django 5.1 and Python 3.11 support
- Email Login via [django-allauth](https://django-allauth.readthedocs.io/en/latest/)
- Integration with `htmx` using `django-htmx`
- [CRUD View Generation](https://falco.oluwatobi.dev/the_cli/crud.html) for your models with optional integrations with `django-tables2` and `django-filters`.
- Built-in **Project Versioning** with `bump2version`, Git integration, automatic changelog updates, and GitHub release creation.
- **Automated Deployment**: Deploy your project to a VPS (using [fabric](https://www.fabfile.org/)) or Docker-based platform with ease.
- Styling with [Tailwind CSS](https://tailwindcss.com/) (including [DaisyUI](https://daisyui.com/)) or [Bootstrap](https://getbootstrap.com/).
- And much more! Check out the full list of packages [here](https://falco.oluwatobi.dev/the_cli/start_project/packages.html)


## 📚 Table of Contents

- [Falco](#falco)
  - [🚀 Features](#-features)
  - [📚 Table of Contents](#-table-of-contents)
  - [📖 Installation](#-installation)
  - [♥️ Acknowledgements](#️-acknowledgements)
  - [👥 Contributors](#-contributors)
  - [📜 License](#-license)

## 📖 Installation

```console
pip install falco-app
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

## 👥 Contributors

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-9-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

<!-- contributors:start -->
Thanks to the following wonderful people [emoji key](https://allcontributors.org/docs/en/emoji-key) who have helped build `falco`.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://oluwatobi.dev"><img src="https://avatars.githubusercontent.com/u/40334729?v=4?s=100" width="100px;" alt="Tobi DEGNON"/><br /><sub><b>Tobi DEGNON</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/commits?author=Tobi-De" title="Code">💻</a> <a href="https://github.com/Tobi-De/falco/commits?author=Tobi-De" title="Documentation">📖</a> <a href="https://github.com/Tobi-De/falco/commits?author=Tobi-De" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hammadarshad1"><img src="https://avatars.githubusercontent.com/u/45298916?v=4?s=100" width="100px;" alt="Muhammad Hammad"/><br /><sub><b>Muhammad Hammad</b></sub></a><br /><a href="#ideas-hammadarshad1" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mathiasag7"><img src="https://avatars.githubusercontent.com/u/50689712?v=4?s=100" width="100px;" alt="mathiasag7"/><br /><sub><b>mathiasag7</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/commits?author=mathiasag7" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://mainlydata.kubadev.com"><img src="https://avatars.githubusercontent.com/u/403435?v=4?s=100" width="100px;" alt="Richard Shea"/><br /><sub><b>Richard Shea</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/commits?author=shearichard" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://lexumsoft.com/"><img src="https://avatars.githubusercontent.com/u/96701299?v=4?s=100" width="100px;" alt="Waqar Khan"/><br /><sub><b>Waqar Khan</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/commits?author=786raees" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tissieres"><img src="https://avatars.githubusercontent.com/u/2410978?v=4?s=100" width="100px;" alt="tissieres"/><br /><sub><b>tissieres</b></sub></a><br /><a href="#financial-tissieres" title="Financial">💵</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://lepture.com"><img src="https://avatars.githubusercontent.com/u/290496?v=4?s=100" width="100px;" alt="Hsiaoming Yang"/><br /><sub><b>Hsiaoming Yang</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/issues?q=author%3Alepture" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aimedey19"><img src="https://avatars.githubusercontent.com/u/89580257?v=4?s=100" width="100px;" alt="Aimé An-Nyong DEGBEY"/><br /><sub><b>Aimé An-Nyong DEGBEY</b></sub></a><br /><a href="#ideas-aimedey19" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/earthcomfy"><img src="https://avatars.githubusercontent.com/u/66206865?v=4?s=100" width="100px;" alt="Hana Belay"/><br /><sub><b>Hana Belay</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/commits?author=earthcomfy" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- contributors:end -->

## 📜 License

`falco` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
