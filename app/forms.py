'''
Input Forms Sheet
'''


from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired

class InputForm(FlaskForm):
    guest_count = IntegerField('Guest Count', validators= [InputRequired()])
    child_count = IntegerField('Child Count', validators= [InputRequired()])
    table_size = IntegerField('Table Size', validators= [InputRequired()])
    child_table_size = IntegerField('Child Table Size', validators= [InputRequired()])

    submit = SubmitField('Submit')


