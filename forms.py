# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 05:10:22 2020

@author: Srishti
"""
""" 
Importing the FlaskForm class from flask_wtf package
Importing StringField class from wtforms package for username, email etc.
Importing PasswordField class from wtforms package for password and password confirmation fields
This allows us to make forms layout using pythom classes representative of forms and then automatically converts it to html templates.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
                          #Type of file it is and validator for allowed file to be uploaded like for image, jpeg and png : after this go to update form.
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User #We import the User model in order to validate it's fields.

"""
Let us make a registration form.
for this we will make a class and inherit the properties of 'FlaskForm' class.
this form will have fields which will also be inherited classes.
"""
class RegistrationForm(FlaskForm):
    """
    1. Let us make a username field first which will be of type StringField.
    2. this Stringfield class is imported from 'wtforms' package not out 'flask_wtf' package, 
       it was automaatically installed with pip install.
    """
    username = StringField('Username', validators=[DataRequired("Username Required"),Length(min=2,max=30)])
    """
    Syntax: variable = Type(name_of_field,)
    name_of_field will also be label in html
    Restrictions over username: Required field, username between 2-20 characters
    To put these checks and validations we can use 'validators' which will be another argument we pass in our field.
    It will be a list of imported validation classes.
    So: 
        1. For username not empty:
            We have the DataRequired validator
            Syntax :
                from wtforms.validators import DataRequired, Length
                
                variable = Type(name_of_field, validators=[DataRequired("message")])
        2. For controlling length of the characters:
            We have the Length validator
            Syntax :
                from wtforms.validators import Length
                
                variable = Type(name_of_field, validators=[Length(min = __, max=__)])
    """
    email = StringField('Email', validators=[DataRequired("Valid Email Address Required"),Email()])
    """
    Syntax: variable = Type(name_of_field,)
    name_of_field will also be label in html
    Restrictions over email: Required field, valid email.
    To put these checks and validations we can use 'validators' which will be another argument we pass in our field.
    It will be a list of imported validation classes.
    So: 
        1. For email not empty:
            We have the DataRequired validator
            Syntax :
                from wtforms.validators import DataRequired, Email
                
                variable = Type(name_of_field, validators=[DataRequired()])
        2. For checking whether it is valid email address or not:
            We have the Email validator
            Syntax :
                from wtforms.validators import Length
                
                variable = Type(name_of_field, validators=[Email()])
    """
    password = PasswordField('Password', validators=[DataRequired("Password Required")])
    """
    Syntax: variable = Type(name_of_field,)
    name_of_field will also be label in html
    Restrictions over password: Required field.
    To put these checks and validations we can use 'validators' which will be another argument we pass in our field.
    It will be a list of imported validation classes.
    So: 
        1. For password not empty:
            We have the DataRequired validator
            Syntax :
                from wtforms.validators import DataRequired
                
                variable = Type(name_of_field, validators=[DataRequired()])
    """
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired("Confirm Password"),EqualTo('password')])
    """
    Syntax: variable = Type(name_of_field,)
    name_of_field will also be label in html
    Restrictions over confirm password: Required field, equal to password
    To put these checks and validations we can use 'validators' which will be another argument we pass in our field.
    It will be a list of imported validation classes.
    So: 
        1. For confirm password not empty:
            We have the DataRequired validator
            Syntax :
                from wtforms.validators import DataRequired
                
                variable = Type(name_of_field, validators=[DataRequired()])
        2. For being equal to password:
            We have the EqualTo validator
            Syntax :
                from wtforms.validators import EqualTo
                
                variable = Type(name_of_field, validators=[EqualTo('name_of_field')])
    """
    submit = SubmitField('Sign Up')
    """
    Syntax: variable = Type(name_of_field)
    name_of_field will also be label in html
    So: 
        Syntax :
            from wtforms import SubmitField
                
            variable = Type(name_of_field/label_of_field)
    """
    
    
    """ 
    We can create a custom validation check function of our own for forms by simply defining functions 
    So, the basic template for validation function for various field is as follows:-
    Syntax:
        def validate_field(self,field):
        if True:
            raise ValidationError('Validation Message')
    
    where:
        field will be like username, email; whichever field we want to validate
        True will be condition we want to test for validation like unique username.
        If it becomes true, then we will give a validation message to the user.
    """
    
    """ So, the first field we want to validate is our username field, whether a user exists or not """
    
    def validate_username(self,username):
        """
        'username.data' --> is what we get from the form field.
        " filter_by(feild_value).first() " --> will return first value from database having the given field_value
        If there is no user , then it returns none
        """
        user = User.query.filter_by(username = username.data).first()
        
        """ 
        Now, we will throw a validation error, if the user exists with that username.
        i.e.:
            user != None (this will throw error)
        """
        if user:
            raise ValidationError('Username already taken')
            
    
    def validate_email(self,email):
        """
        'email.data' --> is what we get from the form field.
        " filter_by(feild_value).first() " --> will return first value from database having the given field_value
        If there is no pre-existing same email , then it returns none.
        """
        user = User.query.filter_by(email = email.data).first()
        
        """ 
        Now, we will throw a validation error, if the user exists with that email address.
        i.e.:
            user != None (this will throw error)
        """
        if user:
            raise ValidationError('The email is linked to an already existing account.')    
            
            

#We will make a similar login form.
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Enter Email"),Email()])
    password = PasswordField('Password', validators=[DataRequired("Enter Password")])
    remember = BooleanField('Remember Me')
    """
    We will make a remember field to login form so that the user remain logged into their accounts for sometime after they close the
    browser using a secure cookie.
    Syntax: variable = Type(name_of_field)
    Syntax:
        from wtforms import BooleanField #This field accepts True/False values only.
                
        variable = Type(name_of_field/label_of_field)
    """
    submit = SubmitField('Login')
    


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png','jpeg'])])
                                                               #list of types of files allowed inside it
                                                               #Syntax: FileAllowed(['file_extension_name'])
                                                               #Example: For pictures we will give an argument like
                                                               #         FileAllowed(['png','jpeg','jpg'])
    submit = SubmitField('Update')

    def validate_username(self, username):
        #the valid username check will only run when the user uses a new username.
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        #the valid email check will only run when the user uses a new email.
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
    
    
    
    
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Post a Picture', validators = [FileAllowed(['jpg','png','jpeg'])])
    submit =  SubmitField('Post')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    