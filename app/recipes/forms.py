from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length,Optional
from flask_wtf.file import FileField, FileAllowed

class RecipeForm(FlaskForm):

    title = StringField("Recipe Title", 
                    validators= [
                        DataRequired(message= "Title is required."),
                        Length(min=1, max=50, message="Title must be under 50 characters!" )
                    ],
                    render_kw={"placeholder": "e.g. Chocolate Cake"}
                    )
    
    description = TextAreaField(
        "Recipe Description (Markdown)",
        validators= [
            DataRequired(message="Description is required!"),
            Length(min=10, max=4000, message="Description must be between 10 and 4000 characters!")
        ],
        render_kw={"placeholder": "Write your recipe here. (In markdown)", "rows": 8}
    )

    category = SelectField(
        "Category",
        validators=[DataRequired(message="Choose a category!")],
        choices=[
            ("","Choose a category"),
            ("Breakfast", "Breakfast"),
            ("Lunch", "Lunch"),
            ("Dinner", "Dinner"),
            ("Dessert", "Dessert"),
            ("Vegan", "Vegan"),
            ("Snacks", "Snacks"),
            ("Other", "Other")
        ]
    )

    image = FileField(
        "Recipe Image",
        validators=[
            FileAllowed(["jpg","jpeg","png"], "Only JPG and PNG images!")
        ]
    )

    submit = SubmitField("Publish Recipe")