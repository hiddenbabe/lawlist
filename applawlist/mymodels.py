import datetime
from email.policy import default
from applawlist import db

class State(db.Model): 
    state_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)

class Services(db.Model): 
    service_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    service_name = db.Column(db.String(255), nullable=False)
    service_cat = db.Column(db.Integer(), db.ForeignKey("service_category.category_id"),nullable=False)

    category = db.relationship("ServiceCategory", backref="services")

class ServiceCategory(db.Model):
    category_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False)
    

class RequestedServices(db.Model):
    idreq = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    job_request_id= db.Column(db.Integer(), db.ForeignKey("service_request.req_id"))
    service_id = db.Column(db.Integer(),db.ForeignKey("services.service_id"),nullable=False)
    
    jobrequest = db.relationship("ServiceRequest", backref="requestedservice")
    servicerequested= db.relationship("Services",backref="jobs_req_service")

class User(db.Model): 
    user_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user_email = db.Column(db.String(255), nullable=True)
    user_pass = db.Column(db.String(255), nullable=False)
    user_fname = db.Column(db.String(255), nullable=False)
    user_lname = db.Column(db.String(255), nullable=False)
    user_mname = db.Column(db.String(255), nullable=True)
    user_image = db.Column(db.String(255), nullable=True)
    user_state = db.Column(db.Integer(), db.ForeignKey("state.state_id"),nullable=False)
    user_lga = db.Column(db.Integer(), db.ForeignKey("lga.lga_id"),nullable=True)
    user_phone = db.Column(db.String(100), nullable=True)
    user_dob = db.Column(db.DateTime(),default=None, nullable=True)
    call_to_bar_year = db.Column(db.DateTime(),nullable=True,default=None)
    type_of_practice = db.Column(db.Enum("Single Practice","Law Firm"),nullable=True)
    area_of_practice = db.Column(db.String(200))
    license_receipt = db.Column(db.String(200))
    bar_certificate = db.Column(db.String(200))
    law_firm_name = db.Column(db.String(200),nullable=True)
    user_address = db.Column(db.Text,nullable=True)
    user_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    status = db.Column(db.Enum("Approved","Not Approved","Suspended"), nullable = False)

    userstate = db.relationship("State",backref="users")


class UserServices(db.Model): 
   user_id = db.Column(db.Integer(), db.ForeignKey("user.user_id"),nullable=False)
   services_id = db.Column(db.Integer(),db.ForeignKey("services.service_id"),nullable=False)  
   userservice_id = db.Column(db.Integer(), primary_key=True,autoincrement=True) 

   users= db.relationship("User", backref="userservices")
   myservice =db.relationship("Services",backref="serviceusers")


class Lga(db.Model): 
    lga_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    lga_name = db.Column(db.String(255),nullable=False)
    state_id = db.Column(db.Integer(),db.ForeignKey("state.state_id"), nullable=False)

class Admin(db.Model): 
    admin = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_username = db.Column(db.String(60),nullable=False)
    pwd = db.Column(db.String(200),nullable=False)

class ServiceRequest(db.Model):
    req_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    requested_by = db.Column(db.Integer(), db.ForeignKey("user.user_id"),nullable=False)
    req_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    job_title = db.Column(db.String(100),nullable=False)
    req_description = db.Column(db.Text,nullable=False)
    state_service_needed = db.Column(db.Integer(),db.ForeignKey("state.state_id"), nullable=False)
    lowest_price= db.Column(db.Float(),nullable = False)
    highest_price= db.Column(db.Float(),nullable = False)
    date_job_start = db.Column(db.DateTime(),nullable=False)
    date_job_end = db.Column(db.DateTime(),nullable=False)
    status = db.Column(db.Enum("active","inactive"),nullable=True,default="active")

    servicerequester = db.relationship("User", backref= "myrequests")
    requeststate = db.relationship("State", backref= "requestsinstate")

class BidRequest(db.Model):
    bid_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    request_id = db.Column(db.Integer(), db.ForeignKey("service_request.req_id"),nullable=False)
    bidder_user = db.Column(db.Integer(), db.ForeignKey("user.user_id"),nullable=False)
    bid_decision = db.Column(db.Enum("Accepted","Declined","Pending"))
    bid_price = db.Column(db.Float(),nullable = False)
    bidder_cv = db.Column(db.String(200), nullable=True)
    bid_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    allrequests = db.relationship("ServiceRequest", backref="allbids")
    bidder = db.relationship("User", backref="mybids")

class Progress(db.Model):
    progress_id= db.Column(db.Integer(),primary_key=True,autoincrement=True)
    job_id = db.Column(db.Integer(), db.ForeignKey("bid_request.bid_id"),nullable=False)
    job_progress = db.Column(db.Enum("Started","In Progress","Completed"))
    updated_by = db.Column(db.Integer(), db.ForeignKey("user.user_id"),nullable=False)
    update_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    currentjob = db.relationship("BidRequest",backref="jobprogress")
    userupdating = db.relationship("User", backref="myjobprogress")

class Messages(db.Model):
    message_id= db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user1 = db.Column(db.Integer(), db.ForeignKey("user.user_id"),nullable=False)
    user2 = db.Column(db.Integer(), db.ForeignKey("user.user_id"),nullable=False)
    content = db.Column(db.Text,nullable=False)
    contactinfo = db.Column(db.String(100),nullable=False)
    message_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    job_id = db.Column(db.Integer(), db.ForeignKey("bid_request.bid_id"),nullable=False)
    status = db.Column(db.Enum("0","1"),nullable=True)

    user_sending = db.relationship("User",backref="messagessent",foreign_keys=user1)
    user_receiving = db.relationship("User",backref="messagesreceived",foreign_keys=user2)
    jobmsg= db.relationship("BidRequest",backref="mymessages")


class Payment(db.Model):
    payment_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    paid_by_user = db.Column(db.Integer(), db.ForeignKey("user.user_id"),nullable=False)
    paid_for_job = db.Column(db.Integer(), db.ForeignKey("bid_request.bid_id"),nullable=False)
    payment_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

class Chat(db.Model):
    chat_id= db.Column(db.Integer(), primary_key=True,autoincrement=True)
    msg_id = db.Column(db.Integer(), db.ForeignKey("messages.message_id"),nullable=False)
    content = db.Column(db.Text,nullable=True)
    chat_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    sender = db.Column(db.Integer(), db.ForeignKey("user.user_id"),nullable=False)
    
    mainmsg = db.relationship("Messages",backref="chats")
    usersending = db.relationship("User",backref="mychats")