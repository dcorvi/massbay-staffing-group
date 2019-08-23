from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('Blog Title', validators=[DataRequired(), Length(max=140, message='Title length must be less than 140 characters')])
    text = TextAreaField('Blog Text', validators=[DataRequired(), Length(max=500, message='Message length must be less than 500 characters')])
    # submit = SubmitField('Post')
