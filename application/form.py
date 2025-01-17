from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class UserInputForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                        choices=[('income', 'Income'), 
                                 ('expense', 'Expense')])
    
    category = SelectField('Category', validators=[DataRequired()],
                        choices=[('rent', 'Rent'), 
                                 ('salary', 'Salary'),
                                 ('investment', 'Investment'),
                                 ('side_hustle', 'Side_hustle')])
    
    amount = IntegerField('Amount', validators=[DataRequired()])

    submit = SubmitField('Generate Report')