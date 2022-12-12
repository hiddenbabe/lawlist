import random
import os,random,string
from flask import Flask,render_template,abort,request,redirect,flash,make_response,session
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from applawlist import myapp,db,mail
from applawlist.mymodels import ServiceCategory, ServiceRequest,User,State,Services,Lga,RequestedServices,BidRequest,Progress, UserServices, Admin, Messages,Chat
from applawlist.forms import JobForm, ProfileForm, BidForm, RegForm

@myapp.route("/")
def home():
   return render_template("index.html")

@myapp.route("/thelawlist/login/",methods=["GET","POST"])
def login():
   form = RegForm()
   if request.method== "GET":
      if session.get("loggedin") == None:
            states=db.session.query(State).all()
            lga=db.session.query(Lga).all()
            return render_template("login.html",states=states,lga=lga,form=form,name="Login")
      else:
         return redirect("/thelawlist/userpage/")
   else:
      username= request.form.get("username")
      pwd = request.form.get("pwd")
      record = db.session.query(User).filter(User.user_email==username).first()
      
      if username== "admin123" and pwd == "1234":
         useradmin = db.session.query(Admin).filter(Admin.admin_username==username).first()
         session["admin"]= useradmin.admin
         return redirect("/thelawlist/admin/admindashboard")
      elif record and check_password_hash(record.user_pass,pwd)== True:
         session['loggedin'] = record.user_id
         return redirect("/thelawlist/userpage/")
      else:
         flash("Invalid credentials, please try again")
         return redirect("/thelawlist/login/")
 

@myapp.route("/thelawlist/signup/",methods=["GET","POST"])
def signup():
      form = RegForm()
      states=db.session.query(State).all()
      lga=db.session.query(Lga).all()
      if request.method=="GET":
         return render_template("signup.html",states=states,lga=lga,form=form,name="Register")
      else:
         fname = request.form.get("fname")
         lname = request.form.get("lname")
         mname = request.form.get("mname")
         email = request.form.get("email")
         pwd = request.form.get("pwd2")
         dob = request.form.get("dob")
         state = request.form.get("state")
         practice= request.form.get("practice")
         lga = request.form.get("lgas")
         firm = request.form.get("lawfirmname")
         address = request.form.get("address")
         phone = request.form.get("phone")
         securepwd = generate_password_hash(pwd)
         u =   User(user_fname=fname,user_lname=lname,user_email=email,user_pass=securepwd,user_mname=mname,user_state=state,user_phone=phone,user_dob=dob,user_address=address,law_firm_name=firm,user_lga=lga,type_of_practice=practice,status="Not Approved")
         db.session.add(u)
         db.session.commit()
         
         msg= Message(subject=f"Welcome to the lawlist {fname} {lname}",sender="thelawlistapp@gmail.com",recipients=[email])
         msg.html = f"<div style='background-color:#03989E;color:white;padding:3%; font-family:'montserrat'><h1 style='color:white;'>The Lawlist<span style='color:#F2712A;'>.</span></h1></div><div>Hello {fname}, thank you for joining the lawist. You can start posting jobs for other lawyers to see on the platform, but if you are interested in providing services to other lawyers you need to complete your profile and upload important documents for review.</div><a href='http://127.0.0.1:8085/thelawlist/update-profile/personal/' style='text-decoration:none'>Update your proile</a> <a href='http://127.0.0.1:8085/thelawlist/post-job/'style='text-decoration:none'>Post a job</a>"
         mail.send(msg)
         return render_template("signupmsg.html")

@myapp.route("/logout/")
def log_out():
   if session.get("loggedin") != None:
      session.pop("loggedin")
   return redirect("/")

@myapp.route("/update-profile/personal/",methods=["GET","POST"])
def update_profile():
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      if request.method == "GET":
         form=ProfileForm()
         
         states=db.session.query(State).all()
         services = db.session.query(Services).all()
         return render_template("update_profile.html",details=details,states=states,form=form,services=services,title= "Update Profile")
      else:
         allowed=[".jpg",".png",".jpeg"]
         profilepic = request.files['pic']
         error=[]
         userobj=db.session.query(User).get(session.get("loggedin"))
         if profilepic != "":
            original_name = profilepic.filename
            filename,extp = os.path.splitext(original_name)
            if extp.lower() in allowed:
               xlist = random.sample(string.ascii_letters,12)
               newfilename = ''.join(xlist) + extp
               image = newfilename
               profilepic.save(f'applawlist/static/uploads/{newfilename}')
               userobj.user_image=image

         state= request.form.get("state")
         phone= request.form.get("phone")
      
         userobj.user_state= state
         userobj.user_phone= phone
         
         db.session.commit()
         flash("Profile successfully updated.")
         return redirect("/update-profile/personal/")
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/update-profile/certificates/",methods=["GET"])
def upload_certificates():
   if session.get("loggedin") != None:
      userobj=db.session.query(User).get(session.get("loggedin"))
      if request.method == "GET":
         form=ProfileForm()
         details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
         return render_template("update_certs.html",details=details,form=form,title= "Update Profile")
   else:
      return redirect("/thelawlist/login/")
   
@myapp.route("/thelawlist/update-profile/certificates/license-receipt",methods=["GET","POST"])
def upload_license():
   if session.get("loggedin") != None:
      userobj=db.session.query(User).get(session.get("loggedin"))
      if request.method == "GET":
         return redirect("/thelawlist/update-profile/certificates/")
      else:
         lawlicense = request.files["licensercpt"]
         if lawlicense:
            original_name_1 = lawlicense.filename
            licensefile,ext1 = os.path.splitext(original_name_1)
            randlist = random.sample(string.ascii_letters,12)
            newfile = ''.join(randlist) + ext1
            newlicense = newfile
            lawlicense.save(f'applawlist/static/uploads/{newfile}')
            userobj.license_receipt=newlicense
            db.session.commit()
            flash("License Receipt Added!")
            return redirect("/thelawlist/update-profile/certificates/")
         else:
            flash("No file was selected")
            return redirect("/thelawlist/update-profile/certificates/")
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/update-profile/certificates/bar-certificate",methods=["GET","POST"])
def upload_bar_certificate():
   if session.get("loggedin") != None:
      userobj=db.session.query(User).get(session.get("loggedin"))
      if request.method == "GET":
         return redirect("/thelawlist/update-profile/certificates/")
      else:
         certificate = request.files["bar_certificate"]   
         if certificate:
            original_name_2 = certificate.filename
            certificatefile,extension = os.path.splitext(original_name_2)
            randomlist = random.sample(string.ascii_letters,12)
            certfile = ''.join(randomlist) + extension
            certificate.save(f'applawlist/static/uploads/{certfile}')
            userobj.bar_certificate=certfile
            db.session.commit()
            flash("Bar Certificate Added!")
            return redirect("/thelawlist/update-profile/certificates/")
         else:
            flash("No file was selected")
            return redirect("/thelawlist/update-profile/certificates/")
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/userpage/",methods=["GET","POST"])
def userpage():
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      activejobs= db.session.query(Progress).filter(Progress.job_progress=="Started").all()
      notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()
      services = db.session.query(UserServices).filter(UserServices.user_id==session.get("loggedin"))
      return render_template("userpage.html",details=details,title= "My Dashboard",activejobs=activejobs,services=services,notifications=notifications)
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/post-job/", methods=["POST","GET"])
def post_job():
   if session.get("loggedin") != None:
      if request.method =="GET":
         form=JobForm()
         states=db.session.query(State).all()
         details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
         notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()
         categories = db.session.query(ServiceCategory).all()
         return render_template("postjob.html",details=details,form=form,categories=categories,states=states,title= "Post A Job",notifications=notifications)
      else:
         start = request.form.get("startdate")
         end = request.form.get("enddate")
         title = request.form.get("title")
         service = request.form.getlist("service")
         user = session.get("loggedin")
         hprice = request.form.get("highprice")
         lprice = request.form.get("lowprice")
         state = request.form.get("state")
         content = request.form.get("description")

         req = ServiceRequest(requested_by=user, req_description=content,lowest_price=lprice,highest_price=hprice,job_title=title,date_job_start=start,date_job_end=end,state_service_needed=state)
         db.session.add(req)
         db.session.commit()

         if req.req_id:
            for p in service:
               servicereq = RequestedServices(job_request_id=req.req_id,service_id=p)
               db.session.add(servicereq)
               db.session.commit()
            

            db.session.add(servicereq)
            db.session.commit()
         
         if servicereq.idreq:
            flash("Job Successfully Posted")
            return redirect("/thelawlist/jobs-posted/")


   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/jobs-posted/",methods=["POST","GET"])
def jobs_posted():
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()
      jobs = ServiceRequest.query.filter(ServiceRequest.requested_by==session.get("loggedin")).order_by(ServiceRequest.req_date.desc()).all()
      # services = db.sesson.query(RequestedServices).filter(RequestedServices.servicerequested.requested_by==session.get("loggedin"))
      return render_template("jobsposted.html",details=details,jobs=jobs,title= "Jobs You've Posted",notifications=notifications)
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/available-jobs/")
def available_jobs():
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      jobs = ServiceRequest.query.filter(ServiceRequest.requested_by!=session.get("loggedin"),ServiceRequest.status=="active").order_by(ServiceRequest.req_date.desc()).all()
      states=db.session.query(State).all()
      services= db.session.query(RequestedServices).all()
      notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()
      return render_template("availablejobs.html",details=details,jobs=jobs,states=states,title= "Available Jobs",services=services,notifications=notifications)
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/getservices/")
def get_services():
   if session.get("loggedin") != None:

      category = request.args.get("category")
      if category != "both":
         record = db.session.query(Services).filter(Services.service_cat==category).all()
      else:
         record = db.session.query(Services).all()
         
      opt = ""

      for r in record:
         opt= opt + f"<div class='col-md-11 option form-control'><input type ='checkbox' value='{r.service_id}' id='option{r.service_id}' class='me-2' name='service'><label for='option{r.service_id}'>{r.service_name}</label></div><br>"
      return opt
   else:
      return redirect("/login/")

@myapp.route("/getlga/")
def getlga():
   stateid = request.args.get("state")
   record = db.session.query(Lga).filter(Lga.state_id==stateid).all()
   opt = ""

   for r in record:
      opt= opt + f"<option value='{r.lga_id}'>{r.lga_name}</option>"
   return opt

@myapp.route("/changejobs/")
def change_jobs():
   if session.get("loggedin") != None:
      userstate = request.args.get("userstate")
      record = db.session.query(ServiceRequest).filter(ServiceRequest.state_service_needed==userstate and ServiceRequest.requested_by!=session.get("loggedin")).all()
      services= db.session.query(RequestedServices).all()
      opt = ""
      if record:
         
         for r in record:
            
            opt= opt + f'<div class="row" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight{r.req_id}" aria-controls="offcanvasRight"><div class="col-md-12 job"><h2 class="mt-5"><a href="#" class="jobtitle">{r.job_title}</a></h2><p>Services Need:</p><p>Budget: &#x20A6;{r.lowest_price} - &#x20A6;{r.highest_price}</p><p>Est Time: {r.date_job_start} - {r.date_job_end}, 20hrs a Week</p> <p>Posted {r.req_date}</p><p><i class="fa-solid fa-location-dot"></i> {r.requeststate.state_name}, Nigeria</p><br><p id="postcontent">{r.req_description}</p><p>Bids:10</p></div></div><div class="offcanvas offcanvas-end fullpost" tabindex="-1" id="offcanvasRight{r.req_id}" aria-labelledby="offcanvasRightLabel"><div class="offcanvas-header"><button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button></div><div class="offcanvas-body p-5"><div class="container mt-2"><div class="row"><div class="col-md-9"><div class="row jobcontent"><div class="col-md-12 p-4"><h3>{r.job_title}</h3></div><div class="col-md-12 p-4"><p>Posted {r.req_date}</p><p><i class="fa-solid fa-location-dot"></i> {r.requeststate.state_name}, Nigeria</p></div></div><div class="row jobheader jobcontent"><div class="col-md-12 p-3"><p>{r.req_description}</p></div></div><div class="row jobheader jobcontent"><div class="col-md-12 p-3 jobtimedeets"><div class="row"><div class="col-md-5"><p class="text-dark"><i class="fa-regular fa-clock"></i> Less than 20 hours a week</p></div><div class="col-md-5"><p class="text-dark"><i class="fa-regular fa-calendar"></i> {r.date_job_start} - {r.date_job_end}</p></div><div class="col-md-5"><p class="text-dark"><i class="fa-solid fa-money-bill-transfer"></i> &#x20A6;{r.lowest_price} - &#x20A6;{r.highest_price}</p></div></div></div></div></div><div class="col-md-3"><button class="applybtn mt-5 p-2"><a href="/thelawlist/{r.req_id}/apply-now/" class="text-light" style="text-decoration:none;">Apply Now</a></button></div></div></div></div></div>'
         return opt
      else:
         opt=opt+ "<h3>No Jobs were found in this location.</h3>"
         return opt
   else:
      return redirect("/login/")

@myapp.route("/changestate/<id>")
def change_state(id):
   if session.get("loggedin") != None:
      newstate = request.args.get("state")
      user_change=db.session.query(User).get(id)
      user_change.user_state = newstate
      db.session.commit()
      return redirect("/thelawlist/available-jobs/")
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/active-jobs/")
def active_jobs():
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      jobs = ServiceRequest.query.order_by(ServiceRequest.req_date.desc()).all()
      states=db.session.query(State).all()
      notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()

      return render_template("availablejobs.html",details=details,jobs=jobs,states=states,title= "Active Jobs",notifications=notifications)
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/active-contracts/")
def active_contracts():
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      contracts = db.session.query(BidRequest).filter(BidRequest.bid_decision=="Accepted")
      notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()
      return render_template("activecontracts.html",details=details,contracts=contracts,title= "Active Contracts",notifications=notifications)
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/getserviceshome/")
def home_services():
   service= db.session.query(Services).all()
   services=""
   for s in service:
      if session.get("loggedin") not in s.serviceusers:
         services+= f'<input type="checkbox" name="service" id="{s.service_name}" class="checkbox" value="{s.service_id}"><label for="{s.service_name}" class="form-control">{s.service_name}</label>'
   services+= '<button type="submit" class="btn mt-2 savebtn" >Save</button>' 
   return services

@myapp.route("/thelawlist/<id>/apply-now/",methods=["POST","GET"])
def apply_now(id):
   if session.get("loggedin") != None:
      records = db.session.query(ServiceRequest).filter(ServiceRequest.req_id==id).all()
      if request.method == "GET":
         if records:
            form = BidForm()
            services= db.session.query(RequestedServices).all()
            notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()
            cat= []
            for x in services:
               if x.servicerequested.service_cat not in cat:
                  cat.append(x.servicerequested.service_cat)
            details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
            category = db.session.query(ServiceCategory).all()
            service_category=[]
            for y in category:
               if y.category_id in cat:
                  service_category.append(y.category_name)

            bids = db.session.query(BidRequest).filter(BidRequest.request_id==id).all()
            bidders=[]
            for bid in bids:
               bidders.append(bid.bidder_user)
            return render_template("applynow.html",details=details,title="Submit A Bid",records=records,services=services,cat=cat,service_category=service_category,form=form,notifications=notifications,bids=bidders)
         else:
            return redirect("/thelawlist/available-jobs/")
      else:
         bid = request.form.get("bid")
         allowed=[".pdf"]
         fileobj = request.files['cv']
         
         if fileobj != "":
            original_name = fileobj.filename
            filename,ext = os.path.splitext(original_name)
            if ext.lower() in allowed:
               xlist = random.sample(string.ascii_letters,12)
               newfilename = ''.join(xlist) + ext
               fileobj.save(f'applawlist/static/uploads/{newfilename}')
               bidreq = BidRequest(request_id=id,bidder_user=session.get("loggedin"),bid_decision="Pending",bid_price=bid,bidder_cv=newfilename)
               db.session.add(bidreq)
               db.session.commit()
               if bidreq.bid_id:
                  flash("Bid submitted successfully!",category="success")
                  return redirect(f"/thelawlist/{id}/apply-now/")
               else:
                  flash("Bid submission unsuccessful. Try again",category="danger")
                  return redirect(f"/thelawlist/{id}/apply-now/")
            else:
               flash("Extension not allowed")
         else:
            flash("Please select a file")

   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/job-bids/<id>",methods=["POST","GET"])
def job_bids(id):
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      records = db.session.query(ServiceRequest).filter(ServiceRequest.req_id==id).all()
      services= db.session.query(RequestedServices).all()
      notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()
      bids = db.session.query(BidRequest).filter(BidRequest.request_id==id).all()
      return render_template("jobbids.html",details=details,title= "Bids",records=records,services=services,bids=bids,notifications=notifications)
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/approve-offer/<id>/<user>/<requestid>",methods=["POST"])
def approve_offer(user,id,requestid):
   if session.get("loggedin") != None:
      if request.method== "GET":
         return redirect("/thelawlist/jobs-posted")
      else:
         msg = request.form.get("message")
         contact = request.form.get("contactinfo")
         message = Messages(user1=session.get("loggedin"),user2=user,content=msg,job_id=id,contactinfo=contact,status="0")
         db.session.add(message)
         db.session.commit()
         approvedbid = db.session.query(BidRequest).filter(BidRequest.bid_id==id).first()
         approvedbid.bid_decision="Accepted"
         db.session.commit()
         declinedbids = db.session.query(BidRequest).filter(BidRequest.request_id==requestid).all()
         for b in declinedbids:
            if b.bid_decision != "Accepted":
               b.bid_decision= "Declined"
         db.session.commit()
         req = db.session.query(ServiceRequest).filter(ServiceRequest.req_id==requestid)
         req.status="inactive"
         db.session.commit()
         flash("You have succesfully accepted an offer")
         return redirect(f'/thelawlist/job-bids/{requestid}')
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/decline-offer/<id>/")
def decline_offer(id):
   if session.get("loggedin") != None:
      users = db.session.query(User).filter(User.user_id==id).first()
      users.status=" Not Approved"
      db.session.commit()
      flash("User status successfully changed!")
      return redirect("/thelawlist/admin/registered-users/")
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/mybids/")
def my_bids():
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()
      bids= db.session.query(BidRequest).filter(BidRequest.bidder_user==session.get("loggedin")).all()
      return render_template("mybids.html",details=details,bids=bids,notifications=notifications)
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/deletebid/<id>")
def delete_bid(id):
   if session.get("loggedin") != None:
      deets= db.session.query(BidRequest).get(id)
      db.session.delete(deets)
      db.commit()
      return redirect("/thelawlist/mybids/")
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/message/")
def messages():
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      services= db.session.query(RequestedServices).all()
      notifications = db.session.query(Messages).filter(Messages.status=="0" , Messages.user2==session.get("loggedin")).all()
      cat= []
      for x in services:
         if x.servicerequested.service_cat not in cat:
            cat.append(x.servicerequested.service_cat)
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      category = db.session.query(ServiceCategory).all()
      service_category=[]
      for y in category:
         if y.category_id in cat:
            service_category.append(y.category_name)
      msg = db.session.query(Messages).filter(Messages.user2==session.get("loggedin"))
      return render_template("messages.html",details=details,msg=msg,title="Messages",services=services,service_category=service_category,notifications=notifications)
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/check-email/")
def check_email():
   email = request.args.get("email")
   user = db.session.query(User).filter(User.user_email==email).first()
   rsp=""
   if user:
      rsp += "Email already in use"
      return rsp
   else:
      return rsp

@myapp.route("/check-number/")
def check_number():
   number = request.args.get("number")
   user = db.session.query(User).filter(User.user_phone==number).first()
   rsp=""
   if user:
      rsp += "Phone number already in use"
      return rsp
   else:
      return rsp


@myapp.route("/readmessage/")
def read_message():
   msg = request.args.get("msgid")
   message = db.session.query(Messages).filter(Messages.message_id==msg).first()
   message.status="1"
   db.session.commit()
   return "done"

@myapp.route("/test/")
def tester():
   details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
   return render_template("tester.html",details=details)


@myapp.route("/sendemail/",methods=["POST","GET"])
def sendemail():
   details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
   if request.method=="GET":
      return render_template("mail.html",details=details)
   else:
      email = request.form.get("email")
      msg= Message(subject="Welcome from the lawlist",sender="thelawlistapp@gmail.com",recipients=[email])
      msg.html = '<div style="background-color:#03989E;color:white;padding:3%" font-family:"montserrat"><h1 style="color:white;">The Lawlist<span style="color:#F2712A;">.</span></h1></div>'
      msg.body = f"Hello ize, thank you for joining the lawist. You can start posting jobs for other lawyers to see on the platform, but if you are interested in providing services to other lawyers you need to complete your profile and upload important documents for review."
      msg.html = "<a href='http://127.0.0.1:8085/thelawlist/update-profile/personal/' style='text-decoration:none'>Update your proile</a> <a href='http://127.0.0.1:8085/thelawlist/post-job/'style='text-decoration:none'>Post a job</a>"
      mail.send(msg)
      mail.send(msg)
      flash("Mail sent!")
      return redirect("/sendemail/")

@myapp.errorhandler(404)
def page_not_found(e):
   if session.get("loggedin") != None:
      details= db.session.query(User).filter(User.user_id==session.get("loggedin")).first()
      return render_template('404.html',title="Page not found",details=details), 404
   else:
      return redirect("/")