# -*- coding: utf-8 -*-
"""
    kb.services
    ~~~~~~~~~~~~~~~~~

    services module
"""

from .users import UserService, RoleService


users = UserService()

roles = RoleService()
