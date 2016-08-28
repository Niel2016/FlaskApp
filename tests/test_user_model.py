import unittest
from app.models import AnonymousUser, Role, Permissions, User


class UserModelTestCase(unittest.TestCase):

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permissions.WRITE_ARTICLES))
        self.assertFalse(u.can(Permissions.MODERATOR))

    def test_anonymous_user(self):

        u = AnonymousUser()
        self.assertFalse(u.can(Permissions.FOLLOWER))
