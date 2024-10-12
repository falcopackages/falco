from __future__ import annotations

import logging

import pytest
from django.http import HttpRequest

pytest_plugins = []


def pytest_configure(config):
    logging.disable(logging.CRITICAL)


@pytest.fixture
def req():
    return HttpRequest()
