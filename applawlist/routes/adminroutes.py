import random
import os,random,string
from flask import Flask,render_template,abort,request,redirect,flash,make_response,session
from werkzeug.security import generate_password_hash, check_password_hash
from applawlist import myapp,db
from applawlist.mymodels import ServiceCategory, ServiceRequest,User,State,Services,Lga,RequestedServices,BidRequest,Progress, UserServices
from applawlist.forms import JobForm, ProfileForm, BidForm

@myapp.route("/thelawlist/admin/admindashboard",methods=["GET","POST"])
def admin_dashboard():
   if session.get("admin") != None:
      return render_template("admin/admin_dashboard.html")
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/thelawlist/admin/registered-users/")
def registered_users():
   if session.get("admin") != None:
      users = db.session.query(User).all()
      return render_template("admin/registered_users.html",users=users)
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/change-status/<id>/")
def change_status(id):
   if session.get("admin") != None:
      users = db.session.query(User).filter(User.user_id==id).first()
      users.status="Approved"
      db.session.commit()
      flash(f"{users.user_fname} {users.user_lname} has been approved successfully.")
      return redirect("/thelawlist/admin/registered-users/")
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/change-status-unapproved/<id>/")
def change_status_2(id):
   if session.get("admin") != None:
      users = db.session.query(User).filter(User.user_id==id).first()
      users.status="Suspended"
      db.session.commit()
      flash(f"{users.user_fname} {users.user_lname} has been supended.")
      return redirect("/thelawlist/admin/registered-users/")
   else:
      return redirect("/thelawlist/login/")

@myapp.route("/all-jobs/")
def all_jobs():
   if session.get("admin") != None:
      jobs = ServiceRequest.query.order_by(ServiceRequest.req_date.desc()).all()
      states=db.session.query(State).all()
      services= db.session.query(RequestedServices).all()
      return render_template("admin/alljobs.html",jobs=jobs,states=states,services=services)
   else:
      return redirect("/thelawlist/login/")

