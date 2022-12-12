from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms import StringField, SubmitField,TextAreaField,SelectField,DateField,IntegerField,EmailField,PasswordField
from wtforms.validators import DataRequired,Length,Email,EqualTo


class ProfileForm(FlaskForm):
   fname = StringField("First Name")
   lname = StringField("Last Name")
   mname = StringField("Middle Name")
   email = EmailField("Email")
   firm = StringField("Law Firm Name")
   phone = StringField("Phone Number",)
   practice = SelectField("Type of practice")
   adress= TextAreaField("Address")
   state = SelectField("State")
   dob= DateField("Date of Birth")
   pic = FileField("Upload Photo",validators=[FileAllowed("jpg","png")])
   licensercpt = FileField("Upload Practice License Receipt",validators=[FileAllowed("pdf","jpg")])
   bar_certificate = FileField("Upload Bar Certificate",validators=[FileAllowed("pdf","jpg")])
   submit = SubmitField("Update Personal info")
   submitdocs = SubmitField("Upload your documents for review")

class JobForm(FlaskForm):
   title = StringField("Write a descriptive title for your post:",validators=[DataRequired(message="Your job post has to have a title."),Length(min=60)])
   description = TextAreaField(validators=[DataRequired(message="You need a job description to complete a job post."),Length(min=60,max=350)])
   submit = SubmitField("Post Job")

class BidForm(FlaskForm):
   bid = IntegerField("What is the amount you would like to bid for this job?",validators=[DataRequired(message="This field cannot be empty"),Length(min=4)])
   cv = FileField("Upload CV",validators=[FileAllowed("pdf"),FileRequired()])
   submit = SubmitField("Submit Bid")

class RegForm(FlaskForm):
   fname = StringField("First Name",validators=[DataRequired(),Length(min=3)])
   lname = StringField("Last Name",validators=[DataRequired(),Length(min=3)])
   mname = StringField("Middle Name",validators=[DataRequired(),Length(min=3)])
   email = EmailField("Email",validators=[DataRequired()])
   firm = StringField("Law Firm Name")
   phone = StringField("Phone Number")
   practice = SelectField("Type of practice",validators=[DataRequired()])
   adress= TextAreaField("Address",validators=[DataRequired()])
   dob= DateField("Date of Birth")
   pwd1 = PasswordField("Password",validators=[DataRequired()])
   pwd2 = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("pwd1")])
   submit = SubmitField("Update Personal info")

   