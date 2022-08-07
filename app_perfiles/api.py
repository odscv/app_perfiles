from __future__ import print_function, unicode_literals

from bs4 import BeautifulSoup
from frappe.model.naming import make_autoname

import frappe
import frappe.defaults
import frappe.permissions
import frappe.share
from frappe import _, msgprint, throw
from frappe.core.doctype.user_type.user_type import user_linked_with_permission_on_doctype
from frappe.desk.doctype.notification_settings.notification_settings import (
	create_notification_settings,
	toggle_notifications,
)
from frappe.desk.notifications import clear_notifications
from frappe.model.document import Document
from frappe.rate_limiter import rate_limit
from frappe.utils import (
	cint,
	escape_html,
	flt,
	format_datetime,
	get_formatted_email,
	has_gravatar,
	now_datetime,
	today,
)
from frappe.utils.password import check_password, get_password_reset_limit
from frappe.utils.password import update_password as _update_password
from frappe.utils.user import get_system_managers
from frappe.website.utils import is_signup_disabled

@frappe.whitelist( allow_guest=True )
def login(usr, pwd):
	try:
		login_manager = frappe.auth.LoginManager()
		login_manager.authenticate(user=usr, pwd=pwd)
		login_manager.post_login()
	except frappe.exceptions.AuthenticationError:
		frappe.clear_messages()
		frappe.local.response["message"] = {
			"success_key":0,
			"message":"Authentication Error!!"
		}

		return

	api_generate = generate_keys(frappe.session.user)
	user = frappe.get_doc('User', frappe.session.user)

	frappe.response["message"] = {
		"success_key":1,
		"message":"Authentication success",
		"sid":frappe.session.sid,
		"api_key":user.api_key,
		"api_secret":api_generate,
		"username":user.username,
		"email":user.email
	}

@frappe.whitelist( allow_guest=True )
def registro(nombres,apellidos,email, redirect_to):
	full_name=nombres+" "+apellidos
	usr_exist = frappe.db.get("User", {"email": email})
	
	if usr_exist:
		if usr_exist.enabled:
			return 0, _("Usuario ya registrado")
		else:
			return 0, _("El usuario ya registrado, pero esta deshabilitado")
	else:
		if frappe.db.get_creation_count("User", 60) > 300:
			frappe.respond_as_web_page(
				_("Temporarily Disabled"),
				_(
					"Too many users signed up recently, so the registration is disabled. Please try back in an hour"
				),
				http_status_code=429,
			)

		from frappe.utils import random_string

		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": escape_html(nombres),
				"last_name":escape_html(apellidos),
				"full_name":escape_html(full_name),
				"enabled": 1,
				"new_password": random_string(10),
				"user_type": "System User",
			}
		)
		
		
		user.flags.ignore_permissions = True
		user.flags.ignore_password_policy = True
		user.insert()
		values = {'email': email}
		
		frappe.db.sql(""" UPDATE tabUser 
				set user_type ='System User',
				owner='Administrator',
				modified_by='Administrator',
				role_profile_name='Postulaciones',
				module_profile='ModulosPostulantes'
				WHERE email = %(email)s """, values=values, as_dict=1)
  
		
		
		idDatosG=frappe.db.sql(""" SELECT tdg.name FROM `tabDatos Generales` tdg  ORDER BY tdg.name  DESC LIMIT 1 """)
		#serieoption=frappe.db.sql(""" SELECT tdf.`options` FROM tabDocField tdf WHERE tdf.fieldname = 'naming_series' and tdf.parent = 'Datos Generales' """, as_dict=0)
		name_datosg=""
		if idDatosG:
			(car,pos)=idDatosG[0][0].split('-')
			x=int(pos)+1
			if len(str(x)) == 1:
				name_datosg=car + "-0000"+str(x)
			if len(str(x)) == 2:
				name_datosg=car + "-000"+str(x)
			if len(str(x)) == 3:
				name_datosg=car + "-00"+str(x)
			if len(str(x)) == 4:
				name_datosg=car + "-0"+str(x)
			if len(str(x)) == 5:
				name_datosg=car + "-" +str(x)
		else:
			name_datosg="POS-00001"
		
		nombrescompletos=escape_html(nombres)+' '+escape_html(apellidos)
		valuesDatosG = {'name':name_datosg,'nombres':escape_html(nombres),'apellidos':escape_html(apellidos),'nombrecompleto':nombrescompletos,'email': email}
		
		#frappe.db.set_value('Datos Generales', name_datosg, {
		#	'docstatus':0,
		#	'idx':0,
		#	'naming_series':"POS-",
		#	'nombres': escape_html(nombres),
		#	'apellidos': escape_html(apellidos),
		#	'nombrecompleto':nombrescompletos,
		#	'email':email
		#})
		frappe.db.sql(""" INSERT INTO `tabDatos Generales` (name,creation,modified,modified_by ,owner ,docstatus,idx,naming_series,nombres,apellidos, nombrecompleto, email) 
                VALUES(%(name)s,NOW(),NOW(),'Administrator','Administrator',0,0,'POS-',%(nombres)s,%(apellidos)s,%(nombrecompleto)s,%(email)s)""", values=valuesDatosG, as_dict=1)
		key = frappe.generate_hash()
		valuesUserP={'name':key,'user':email,'for_value':name_datosg}
		frappe.db.sql(""" INSERT INTO `tabUser Permission` (name,creation,modified ,modified_by,owner,docstatus,idx,`user`,allow,for_value,is_default,apply_to_all_doctypes)
VALUES(%(name)s,NOW(),NOW(),'Administrator','Administrator',0,0,%(user)s,'Datos Generales',%(for_value)s,0,1) """,values=valuesUserP, as_dict=1)
		#if redirect_to:
		#    frappe.cache().hset("redirect_after_login", user.name, redirect_to)

		if user.flags.email_sent:
			return 1, _("Please check your email for verification")
		else:
			return 2, _("Please ask your administrator to verify your sign-up")
		
	

def generate_keys(user):
	user_details = frappe.get_doc('User', user)
	api_secret = frappe.generate_hash(length=15)

	if not user_details.api_key:
		api_key = frappe.generate_hash(length=15)
		user_details.api_key = api_key

	user_details.api_secret = api_secret
	user_details.save()

	return api_secret


@frappe.whitelist(allow_guest=True)
def update_password(new_password, logout_all_sessions=0, key=None, old_password=None):
	# validate key to avoid key input like ['like', '%'], '', ['in', ['']]
	if key and not isinstance(key, str):
		frappe.throw(_("Invalid key type"))

	result = test_password_strength(new_password, key, old_password)
	feedback = result.get("feedback", None)

	if feedback and not feedback.get("password_policy_validation_passed", False):
		handle_password_test_fail(result)

	res = _get_user_for_update_password(key, old_password)
	if res.get("message"):
		frappe.local.response.http_status_code = 410
		return res["message"]
	else:
		user = res["user"]

	logout_all_sessions = cint(logout_all_sessions) or frappe.db.get_single_value(
		"System Settings", "logout_on_password_reset"
	)
	_update_password(user, new_password, logout_all_sessions=cint(logout_all_sessions))

	user_doc, redirect_url = reset_user_data(user)

	# get redirect url from cache
	redirect_to = frappe.cache().hget("redirect_after_login", user)
	if redirect_to:
		redirect_url = redirect_to
		frappe.cache().hdel("redirect_after_login", user)

	frappe.local.login_manager.login_as(user)

	frappe.db.set_value("User", user, "last_password_reset_date", today())
	frappe.db.set_value("User", user, "reset_password_key", "")
	values = {'user': user}
	frappe.db.sql(""" UPDATE tabUser 
				set user_type ='System User',
				owner='Guest',
				role_profile_name='Postulaciones',
				module_profile='ModulosPostulantes'
				WHERE email = %(user)s """, values=values, as_dict=1)
	
	if user_doc.user_type == "System User":
		return "/app"
	else:
		return redirect_url if redirect_url else "/"

def handle_password_test_fail(result):
	suggestions = result["feedback"]["suggestions"][0] if result["feedback"]["suggestions"] else ""
	warning = result["feedback"]["warning"] if "warning" in result["feedback"] else ""
	suggestions += (
		"<br>" + _("Hint: Include symbols, numbers and capital letters in the password") + "<br>"
	)
	frappe.throw(" ".join([_("Invalid Password:"), warning, suggestions]))

@frappe.whitelist(allow_guest=True)
def test_password_strength(new_password, key=None, old_password=None, user_data=None):
	from frappe.utils.password_strength import test_password_strength as _test_password_strength

	password_policy = (
		frappe.db.get_value(
			"System Settings", None, ["enable_password_policy", "minimum_password_score"], as_dict=True
		)
		or {}
	)

	enable_password_policy = cint(password_policy.get("enable_password_policy", 0))
	minimum_password_score = cint(password_policy.get("minimum_password_score", 0))

	if not enable_password_policy:
		return {}

	if not user_data:
		user_data = frappe.db.get_value(
			"User", frappe.session.user, ["first_name", "middle_name", "last_name", "email", "birth_date"]
		)

	if new_password:
		result = _test_password_strength(new_password, user_inputs=user_data)
		password_policy_validation_passed = False

		# score should be greater than 0 and minimum_password_score
		if result.get("score") and result.get("score") >= minimum_password_score:
			password_policy_validation_passed = True

		result["feedback"]["password_policy_validation_passed"] = password_policy_validation_passed
		return result

def _get_user_for_update_password(key, old_password):
	# verify old password
	result = frappe._dict()
	if key:
		result.user = frappe.db.get_value("User", {"reset_password_key": key})
		if not result.user:
			result.message = _("The Link specified has either been used before or Invalid")

	elif old_password:
		# verify old password
		frappe.local.login_manager.check_password(frappe.session.user, old_password)
		user = frappe.session.user
		result.user = user

	return result

def reset_user_data(user):
	user_doc = frappe.get_doc("User", user)
	redirect_url = user_doc.redirect_url
	user_doc.reset_password_key = ""
	user_doc.redirect_url = ""
	user_doc.save(ignore_permissions=True)

	return user_doc, redirect_url