from __future__ import annotations

from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavItem


class MainNav(Nav):
    template_name = "partials/navigation.html"
    items = [
        NavItem(title="Dashboard", url="/tailwind/"),
        NavItem(title="Team", url="#"),
        NavItem(title="Projects", url="#"),
        NavItem(title="Calendar", url="#"),
    ]
