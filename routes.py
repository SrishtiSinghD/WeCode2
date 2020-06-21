# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 02:15:30 2020

@author: Srishti
"""

from PIL import Image
#We will import Image class from Pillow library to resize the profile picture for saving storage space in our database.
#After installing this, go to the 'save_picture' function to resize the picture uploaaded by the users.

import os
#This will be required to get the file extension of file uploaded by the user, in the 'save_picture' function.


import secrets
#this module will be used to create random image name for our 'save_picture' function.

from flask import render_template, url_for, flash  ,redirect , request
"""
import 'render_template' class to import templates made by us.
'url_for' is used for linking webpages for us in our html files.
'flash' to flash error messages to user
'redirect' for redirecting to other url page, it takes 'url_for' as an argument
'request' for getting query parameter 'next' which is equal to the page we wanted to access but failed to do so due to not being logged in.
we can then use it after login to redirect the user to the page stored in 'next' query parameter.
"""

from project import app, db, bcrypt

from project.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
"""
Now, we wil import the forms we made in 'forms.py' file
Since, both our files are in same directory, we will directly write the following syntax:
    from file_name import class_name(s)
    
    Eg: 
        from forms import RegistrationForm, LoginForm

After this create routes for these forms to be converted to HTML first.
"""


from project.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

"""
#dummy data created a list of dictionaries, to show how to make dynamic webpages.

Here we called a database 
and got back a list of posts in the form of dictionaries.
-->
posts_list = [
        
        {   #Each dictionary represent a single blog post/content.
            'author':'Srishti Singh',
            'title':'blogpost 1',
            'content':'First Post Content',
            'date_posted':'28/4/2020'   
        },
        
        {
            'author':'Dhruv Singh',
            'title':'blogpost 2',
            'content':'Second Post Content',
            'date_posted':'28/4/2020'   
        }
        
]
"""

#after we made this dummy data, let's pass this as an argument in our "render_template" funaction

"""
# routes are what we type onto our browser to go to different pages within a website. These are called decorators
#learn decorators : 
they add additional functionality to existing function
here, this app.route decorator handles all the complicated backend stuff 
and allow us to write a simple function that returns the information to be shown on our website for this specific page/route
"""

#route for the home page or starting page
#both / and /home will navigate to the same page 
@app.route('/')                                
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home_inherited.html', posts_var=posts)

#route for about page
@app.route('/about')
def about():  #always change function name for new page
    return render_template('about_inherited.html',title="About")
"""
PASSING OF HTML CODE FOR THE STATIC WEBPAGE
There are two ways:-
    1. Pass code directly in python file:
        @app.route('/webpage')
        def about():  
            return '''
                    TYPE YOUR ENTIRE HTML CODE HERE.            
            '''
    2. Pass name of the file stored in templates folder:
        @app.route('/webpage')
        def about():  
            return render_template('webpage.html') 
        
        NOTE:- The webpage's html file must be stored in the folder named "templates" within your project directory.
               "project_folder/templates/webpage.html"
               The folder "templates" name should be all in lowercase.

PASSING OF HTML CODE FOR THE DYNAMIC WEBPAGE
We will pass two arguments to the "render_template" function.
Argument1 --> Name of the html file.
Argument2 --> A variable storing the list of posts/other dynamic content(Like above we created a dummy data named posts).
              This second variable can directly be accessed in our html file, 
              which will help in looping over each post stored in our database, and retrieved here in the form of list of dictionaries here.
Argument3 --> We can also pass a title to our webpage using this.             
SYNTAX:
    @app.route('/webpage')
        def about():  
            return render_template('webpage.html', variable_for_posts=list_of_data, variable_for_title="Title")
            
    After this, to display each post stored in the list "posts_list", we surely need a for loop.
    But that for loop will be created in our html file not here :).
    So, now switch over to your html file and write the following code in your html file under the <body> tag.

"""

#routes for the registration form
@app.route('/register', methods=['GET','POST']) #This method allow us to post data and get data from a page
def register():
    """ 
    This will rediirect a logged-in user to home-page when they click the register button on our site
    Here, 'current_user.is_authenticated' is a boolean variable.
    """ 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    """
    We will create an instance of a registration form everytime to send to the application.
    """
    form = RegistrationForm()
    """
    Now, we need to validate the data we are getting from the user, so we will first validate data and then post template.
    We will also flash an alert message to user on invalid entry using the 'flash' class in Flask.
    """
    if form.validate_on_submit():
        
        """ 
        So, after the form is validated, firstly we will save the password entered by the user in the database , in hashed form.
        Here, we will be first passing the password entered by the user to the 'generate_password_hash()' function in bcrypt class
        it will return hashed password in form of bytes.
        To convert the hashed password in form of string we will use the 'decode.('utf-8') method .
        Syntax:
            variable_storing_hashed_password = bcrypt.generate_password_hash('password_string').decode('utf-8')
        """
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        """ After storing the hashed password we will create a user instance """
        user = User(username = form.username.data , email = form.email.data , password = hashed_password)
        
        """ Next, we are going to add this user to our database """
        db.session.add(user)
        
        """ In order to actually show those changes in our database, we use the commit command """
        db.session.commit()
        
        flash('Your account has been successfully created! You are now able to log in', 'success') 
        #flash(f'Account created for {form.username.data} !', 'success') 
        """
        (f) string is available from Python 3.6 as a replacement for (format) to access variables in strings.
        Users below Python 3.6 should use format specifiers.
        flash('Message','Bootstrap_Style_for_Message')
        Like here our Message == 'Account created for {form.username.data}!'
        Bootstrap_Style_for_Message == 'success'
        These flashed messages are a one-time alert, they disappear when you reload the same window.
        """
        
        
        """
        CODE FOR TRIAL:-
        Now we need to redirect the user to the home page after successful form completion
        For this we import redirect class from Flask

        return redirect(url_for('home')) 
        """
    
        """
        Now we need to redirect the user to the home page after successful form completion
        For this we import redirect class from Flask
        """
        return redirect(url_for('login'))
    
    #Here, we will pass this form to our HTML Template
    return render_template('register.html', title='Register', form=form)

#routes for the login form
@app.route('/login', methods=['GET','POST'])
def login():
    """ 
    This will rediirect a logged-in user to home-page when they click the login button on our site
    Here, 'current_user.is_authenticated' is a boolean variable.
    """ 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    """
    We will create an instance of a login form everytime to send to the application.
    """
    form = LoginForm()
    if form.validate_on_submit():
        """
        Authenticating user to login using manual dummy data
        if form.email.data == 'ayz@gmail.com' and form.password.data == 'password':
            flash('You have been Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger') # category to flash alert in bootstrap.
        """
        """ Authenticating user login using data stored in our database. """
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data) #logs in the user.
            #now we will check for any redirection query parameter (like next)
            next_page = request.args.get('next')
            """
            Here, 'args' is a dictionary and we don't want to access whole dictionary as well as it is optional
            So, we use the 'get' method in dictionary so that when 'next' is not found, then it returns 'none' instead of throwing errors.
            """
            return redirect(next_page) if next_page else redirect(url_for('home'))
                   #This is actually an example of using ternary conditional operator in python
                   #condition ? if : else
        else:    
            flash('Login Unsuccessful. Please check email and password', 'danger') # category to flash alert in bootstrap.
    #After this we will pass this form to our HTML Template
    return render_template('login.html', title='Login', form=form)

""" We are ready to go to make the HTML templates for both Registration and Login Form. """

#route for the logout button
@app.route('/logout')
def logout():
    logout_user() #logouts the user
    return redirect(url_for('home')) #This redirects the user to home page when logout button is clicked.



#This function will save the image uploaded by the user in our filesystem
#Module used : secrets(random name for picture), os(to get file extension)
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #will create a random token of 8 bytes
    """ 
    Now, to get the extension of the file, we will use the os module's path.splitext()function,
    which will give us a tuple of filename and extension
    Syntax:
        tuple_variable = os.path.splitext(file_name)
    Example:
        Here. to accept the picture we will type it as:
            picture_file_name , picture_file_extension = os.path.splitext(picture_filename)
    """
    #f_name, f_ext = os.path.splitext(form_picture.filename)
    # We use '_' for the file_name variable as we won't be using this variable and our editor will also not show the "unused variable" warning.
    #This is a popular way among python developers to throw away a variable
    _, f_ext = os.path.splitext(form_picture.filename)
    """
    form_picture = data we get from the form field
    filename = it's an attribute of that form field if it is of type file, it is there by default
    """
    picture_fn = random_hex + f_ext #We renamed our uploaded file.
    
    #Path to save this image
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    """ app.root_path --> it gives path of our package directory
        'static/profile_pics' --> path where profile pic is stored
        'picture_fn' --> random picture name we created
        "os.path.join" --> This will make a whole path as we provided by joining the above three strings we provided.
    """
    
    """ Before saving the picture, resize it to save your storage space in the database. """
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    
    """ Now, we will save this resized picture instead of the whole picture uploaded by the user."""
    i.save(picture_path)
    
    
    #form_picture.save(picture_path)
    
    #This way we saved the picture to our file system
    return picture_fn 
    #This function saves the file and returns the file name.
    
#route for the account page which the user can access only when he/she is logged in. 
@app.route('/account', methods=['GET','POST'])
#this 'login_required' extension will make it mandatory for the user to be logged-in to access the account page
#and this will require a page to produce in response to invalid 'account' access, for which create a variable in init file
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            db.session.commit()
            flash('Profile Picture updated' , 'success')
        if current_user.username != form.username.data:
            current_user.username = form.username.data
            db.session.commit()
            flash('Account Username has been updated successfully' , 'success')
        if current_user.email != form.email.data:
            current_user.email = form.email.data
            db.session.commit()
            flash('Account Email has been updated successfully' , 'success')
        return redirect(url_for('account')) 
        #redirected to account page with successful submit data. "Are you sure you want to reload, data need to be resubmitted." will not occur
        #This way our browser will also send a get request to server otherwise down with
        #render_template, it would have just sent a post request.
    
    #To print current user details, already in our form fields
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/'+current_user.image_file) # Passing the user's image.
    return render_template('account.html', title='Account', image_file = image_file, form=form) 
# This will display the 'account.html' template with page title as Account.
    



def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)
    
    output_size=(500,500)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    #form_picture.save(picture_path)

    return picture_fn



#We are creating the create post page now:
@app.route("/post/new", methods=['GET','POST'])
#Now, we will add a decorator to allow the user to create post, only when logged in.
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
           picture_file = save_post_picture(form.picture.data)
           post = Post(title=form.title.data, content=form.content.data, image_file=picture_file, author=current_user)
           db.session.add(post)
           db.session.commit()
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
        flash('Your post has been created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form) 

"""
Here, <post_id> is a variable which will enable us to route to a specific post
For e.g., "/post/1" means we are  currently viewing the post with id=1
We can even specify the type of our 'post_id' variable by using the following syntax:
    @app.route("/post/<variable_type:variable_name>")
"""
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    """ 'get_or_404' --> either give me a method with id=post_id or return 404error which means that the post doesn't exist """
    return render_template('post.html', title=post.title, post=post)
















