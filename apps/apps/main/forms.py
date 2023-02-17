from starlette_wtf import StarletteForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import (
    AnyOf, DataRequired, Email, EqualTo, Length
)


class LoginForm(StarletteForm):
    username = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class RegisterForm(StarletteForm):
    email = StringField(
        'Email address',
        validators=[
            DataRequired('Please enter your email address'),
            Email()
        ])
    username = StringField(
        'Username', validators=[
            DataRequired('Please enter your username'),
            Length(min=4, max=150, message='Minimal 4 characters')
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired('Please enter your password'),
            Length(min=8, message='Minimal 8 characters')
        ])
    confirm = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired('Please confirm your password'),
            EqualTo('password', message='Passwords must match'),
        ]
    )

    name = StringField(
        'Name', validators=[
            DataRequired('Your Full name'),
            Length(max=150, message='Minimal 4 characters')
        ])

    agree_terms = BooleanField(
        'Agree terms', validators=[
            AnyOf([True, 1], message='Agree to the terms is required to register')
        ])


class ForgotPasswordForm(StarletteForm):
    email_username = StringField(
        'Email or Username', validators=[DataRequired()]
    )


class ResetPasswordForm(StarletteForm):
    password = PasswordField(
        'Password',
        validators=[
            DataRequired('Please enter your password'),
            Length(min=8, message='Minimal 8 characters')
        ])
    confirm = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired('Please confirm your password'),
            EqualTo('password', message='Passwords must match'),
        ]
    )
