from payments.models import User
import factory


class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User
	name = 'test_fac'
	email = 'test_fac@t.com'
	id = 0
	password = "1234"
	last_4_digits = '3333'
	stripe_id = 1