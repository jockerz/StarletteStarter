from starlette_babel import gettext_lazy as _
from starlette_wtf import StarletteForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import (
    AnyOf, DataRequired, Email, EqualTo, Length
)


class LoginForm(StarletteForm):
    username = StringField(_('Email or Username'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_('Remember Me'))


class RegisterForm(StarletteForm):
    email = StringField(
        _('Email address'),
        validators=[
            DataRequired(_('Please enter your email address')),
            Email()
        ])
    username = StringField(
        'Username', validators=[
            DataRequired(_('Please enter your username')),
            Length(min=4, max=150, message=_('Minimal 4 characters'))
        ])
    password = PasswordField(
        _('Password'),
        validators=[
            DataRequired(_('Please enter your password')),
            Length(min=8, message=_('Minimal 8 characters'))
        ])
    confirm = PasswordField(
        _('Confirm Password'),
        validators=[
            DataRequired(_('Please confirm your password')),
            EqualTo('password', message=_('Passwords must match')),
        ]
    )

    name = StringField(
        'Name', validators=[
            DataRequired(_('Your Full name')),
            Length(max=150, message=_('Minimal 4 characters'))
        ])

    agree_terms = BooleanField(
        _('Agree terms'), validators=[
            AnyOf([True, 1], message=_('Agree to the terms is required to register'))
        ])


class ForgotPasswordForm(StarletteForm):
    email_username = StringField(
        'Email or Username', validators=[DataRequired()]
    )


class ResetPasswordForm(StarletteForm):
    password = PasswordField(
        _('Password'),
        validators=[
            DataRequired(_('Please enter your password')),
            Length(min=8, message=_('Minimal 8 characters'))
        ])
    confirm = PasswordField(
        _('Confirm Password'),
        validators=[
            DataRequired(_('Please confirm your password')),
            EqualTo('password', message=_('Passwords must match')),
        ]
    )
