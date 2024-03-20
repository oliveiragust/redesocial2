from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class PostForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class FollowForm(FlaskForm):
    submit = SubmitField('Follow')