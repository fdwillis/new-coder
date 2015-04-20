from payments.models import User
import factory


class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User
	email = 'test_fac@t.com'
	id = 1