from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import UserType


class HasNormalUserAccess(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.normal.value
        return False


class HasAdminAccess(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.admin.value
        return False

class HasSupportAccess(UserPassesTestMixin):
    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.support.value
        return False


class HasCompanyAccess(UserPassesTestMixin):
    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.company.value
        return False
