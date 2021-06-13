from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, Optional


class CustomRadioField(RadioField):

    def pre_validate(self, form):
        pass

class CustomSelectField(SelectField):

    def pre_validate(self, form):
        pass



class ArrangementForm(FlaskForm):
    arrangement = CustomRadioField('Arrangement',  choices=[("Basement", "Basement"), ("Condo", "Condo")])
    province = CustomSelectField("Province",  choices=[("Ontario", "Ontario")] )


class HomeownerLocationCondoForm(FlaskForm):

    streetNumber = IntegerField('Street Number', 
    validators=[InputRequired("Please enter a street number")], 
    render_kw={"icon": "home", "required": False, "helperText": "Ex. 1234"})

    streetName = StringField('Street Name', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=200, message="Please enter a street name less that 200 characters.")], 
    render_kw={"icon": "home", "required": False, "helperText": "Ex. Front St."})

    city = StringField('City', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=100, message="Please enter a city less that 100 characters.")], 
    render_kw={"icon": "location_city", "required": False, "helperText": "Ex. Toronto"})

    postalCode = StringField('Postal Code', 
    validators=[InputRequired("Please enter a postal code"), Length(min=1, max=10, message="Please enter a postal code less that 10 characters.")], 
    render_kw={"icon": "markunread_mailbox", "required": False, "helperText": "Ex. L1T 0E2"})

    poBox = StringField('P.O. Box', 
    validators=[InputRequired("Please enter a P.O. Box")], 
    render_kw={"icon": "markunread_mailbox", "required": False, "helperText": "Ex. 1234"})

    unitNumber = StringField('Unit Number', 
    validators=[InputRequired("Please enter a unit number"), Length(min=1, max=10, message="Please enter a unit number less that 10 characters.")], 
    render_kw={"icon": "home", "required": False, "helperText": "Ex. 1234"})


class HomeownerLocationBasementForm(FlaskForm):

    streetNumber = IntegerField('Street Number', 
    validators=[InputRequired("Please enter a street number")], 
    render_kw={"icon": "home", "required": False, "helperText": "Ex. 1234"})

    streetName = StringField('Street Name', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=200, message="Please enter a street name less that 200 characters.")], 
    render_kw={"icon": "home", "required": False, "helperText": "Ex. Front St."})

    city = StringField('City', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=100, message="Please enter a city less that 100 characters.")], 
    render_kw={"icon": "location_city", "required": False, "helperText": "Ex. Toronto"})

    postalCode = StringField('Postal Code', 
    validators=[InputRequired("Please enter a postal code"), Length(min=1, max=10, message="Please enter a postal code less that 10 characters.")], 
    render_kw={"icon": "markunread_mailbox", "required": False, "helperText": "Ex. L1T 0E2"})

 
class RentalUnitLocationForm(FlaskForm):
    streetNumber = IntegerField('Street Number', 
    validators=[InputRequired("Please enter a street number")], 
    render_kw={"icon": "home", "required": False, "helperText": "Ex. 1234"})

    streetName = StringField('Street Name', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=200, message="Please enter a street name less that 200 characters.")], 
    render_kw={"icon": "home", "required": False, "helperText": "Ex. Front St."})

    city = StringField('City', 
    validators=[InputRequired("Please enter a street name"), Length(min=1, max=200, message="Please enter a city less that 100 characters.")], 
    render_kw={"icon": "location_city", "required": False, "helperText": "Ex. Toronto"})

    postalCode = StringField('Postal Code', 
    validators=[InputRequired("Please enter a postal code"), Length(min=1, max=200, message="Please enter a postal code less that 10 characters.")], 
    render_kw={"icon": "markunread_mailbox", "required": False, "helperText": "Ex. L1T 0E2"})


        
