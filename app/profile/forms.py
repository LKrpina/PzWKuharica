from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length

class ProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField("About Me", validators=[Length(max=300)])
    date_of_birth = DateField("Date of Birth", format="%Y-%m-%d")
    profile_image = FileField("Profile Image", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Save Changes")

