import pytest

from accounts.models import Manager, User


@pytest.mark.django_db
def test_user_creation_signal():
    user = User(email='test@test.com', user_type='manager', password='testing')
    user.save()

    manager = Manager.objects.get(user__email='test@test.com')

    assert User.objects.count() == Manager.objects.count()
    assert user.email == manager.user.email