from django.contrib.auth.forms import UserChangeForm
from annotations.models import VogonUser
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms
from crispy_forms.helper import FormHelper

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# class CrispyUserChangeForm(UserChangeForm):
# 	password = None		# This field was set in the Form ancestor, so exclude
# 						#  is insufficient.
#
# 	class Meta:
# 		model = User
# 		exclude = ['password', 'groups', 'user_permissions', 'last_login',
# 				   'is_staff', 'is_superuser', 'date_joined', 'is_active',
# 				   'username']
#
# 	def __init__(self, *args, **kwargs):
# 		super(CrispyUserChangeForm, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper(self)


class RegistrationForm(forms.Form):
	"""
	Gives user form of signup and validates it.
	"""
	full_name = forms.CharField(required=True, max_length=30, label=_("Full name"))
	username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"),
                                error_messages={ 'invalid': _("This value must contain only letters, "
                                                              "numbers and underscores.") })
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30,
                                                                      render_value=False)), label=_("Password"))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30,
                                                                      render_value=False)), label=_("Password (again)"))
	affiliation = forms.CharField(required=True, max_length=30, label=_("Affliation"))
	location = forms.CharField(required=True, max_length=30, label=_("Location"))


	def clean_username(self):
		"""
		Validates username.
		"""
		try:
			user = VogonUser.objects.get(username__iexact=self.cleaned_data['username'])
		except VogonUser.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError(_("The username already exists. Please try another one."))

	def clean(self):
		"""
		Validates the values inserted in Password and Confirm Password field are same.
		"""
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_("The two password fields did not match."))

def validatefiletype(file):
	"""
	Validates type of uploaded file.

	Parameters
	----------
	file : file
		The file that is uploaded.

	Raises
	------
	ValidationError
		Raises this exception if uploaded file is neither plain text nor PDF
	"""
	if file.content_type != 'application/pdf' and file.content_type != 'text/plain':
		raise ValidationError('Please choose a plain text file or PDF file')

class UploadFileForm(forms.Form):
	title = forms.CharField(label='Title:', max_length=255, required=True)
	ispublic = forms.BooleanField(label='Make this text public?',
				required=False,
				help_text='By checking this box you affirm that you have the\n'+
						  'right to make this file publicly available.')
	filetoupload = forms.FileField(label='Choose a file (plain text or PDF):',
				required=True,
				validators=[validatefiletype])
	datecreated = forms.DateField(label='Date created:',
				required=False,
				widget=forms.TextInput(attrs={'class':'datepicker'}))


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = VogonUser
        fields = ('full_name', 'email', 'affiliation', 'location', 'link', 'imagefile')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = VogonUser
        fields = ('full_name', 'email', 'affiliation', 'location','imagefile')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get("password")

    def clean_full_name(self):
        if not self.cleaned_data.get('full_name'):
            raise ValidationError(_('Missing full name.'), code='required')
        else:
        	return self.cleaned_data['full_name']

    def clean_email(self):
        if not self.cleaned_data.get('email'):
            raise ValidationError(_('Missing email.'), code='required')
        else:
        	return self.cleaned_data['email']

    def clean_location(self):
        if not self.cleaned_data.get('location'):
            raise ValidationError(_('Missing location.'), code='required')
        else:
        	return self.cleaned_data['location']

    def clean_affiliation(self):
        if not self.cleaned_data.get('affiliation'):
            raise ValidationError(_('Missing affiliation.'), code='required')
        else:
        	return self.cleaned_data['affiliation']


    
