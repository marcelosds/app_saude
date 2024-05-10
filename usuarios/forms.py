from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm as AuthSetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class PasswordResetRequestForm(PasswordResetForm):
    email = forms.EmailField(max_length=254)

    def send_email(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        # Send an email to the user with the password reset link.
        context['user'] = self.user
        context['token'] = default_token_generator.make_token(self.user)
        context['uid'] = urlsafe_base64_encode(force_bytes(self.user.pk))
        super().send_email(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name)

class SetPasswordForm(AuthSetPasswordForm):
    # You can customize this form as needed
    pass