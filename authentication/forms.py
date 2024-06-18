from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form.

    This form is used to create a new user. It extends the UserCreationForm
    from django.contrib.auth.forms and adds the 'username' field.
    """

    # Add 'username' field to the form
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='',
        validators=[validate_slug],
    )

    # Add 'password1' and 'password2' fields to the form
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="",
        error_messages={'required': ''}
    )
    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput,
        help_text="",
        error_messages={'required': ''}
    )

    class Meta(UserCreationForm.Meta):
        """
        Meta options for the form.

        This class sets the model to CustomUser and adds the 'email' field to
        the fields.
        """
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_username(self):
        """
        Validate the username.

        This method checks if the username contains '@' or '/' characters. If
        it does, it raises a ValidationError. It also checks if the username
        already exists in the CustomUser model and raises a ValidationError if
        it does.

        Returns:
            str: The validated username.
        """
        # Get the cleaned username from the form data
        username = self.cleaned_data.get('username')

        # Check if the username contains '@' or '/' characters
        if '@' in username or '/' in username:
            # Raise a ValidationError if it does
            raise ValidationError("Username should not contain '@' or '/' characters.")

        # Prepend '@' to the username
        username = '@' + username

        # Check if the username already exists in the CustomUser model
        if CustomUser.objects.filter(username=username).exists():
            # Raise a ValidationError if it does
            raise ValidationError("Username already exists!")

        # Return the validated username
        return username



class CustomUserChangeForm(UserChangeForm):
    """
    Custom UserChangeForm for the CustomUser model.

    This form is used to update the details of a CustomUser. It extends the
    UserChangeForm from django.contrib.auth.forms and adds the 'email' field
    to the fields.
    """

    class Meta:
        # Set the model to CustomUser
        model = CustomUser

        # Add the 'email' field to the fields
        fields = UserChangeForm.Meta.fields

class ProfileUpdateForm(forms.ModelForm):
    """
    ModelForm for updating the details of a CustomUser.

    This form is used to update the details of a CustomUser and is overridden to
    exclude the 'username' field.
    """

    class Meta:
        # Set the model to CustomUser
        model = CustomUser

        # Set the fields to be updated
        fields = ['first_name', 'last_name', 'email', 'profile_image', 'bio']

    def __init__(self, *args, **kwargs):
        """
        Override the constructor to modify the form fields.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Call the parent class constructor
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        # Set the 'email' field as not required
        self.fields['email'].required = False
        # The 'email' field is not required in this form because it is already
        # associated with the user and is not meant to be modified here.
