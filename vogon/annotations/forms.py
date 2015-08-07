from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper

class CrispyUserChangeForm(UserChangeForm):
	password = None		# This field was set in the Form ancestor, so exclude
						#  is insufficient.

	class Meta:
		model = User
		exclude = ['password', 'groups', 'user_permissions', 'last_login',
				   'is_staff', 'is_superuser', 'date_joined', 'is_active',
				   'username']

	def __init__(self, *args, **kwargs):
		super(CrispyUserChangeForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
