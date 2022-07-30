from __future__ import unicode_literals
import frappe
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
 
sitemap = 1

def get_context(context):
    context.show_search = True
    context.allow_guest = True
    context.no_breadcrumbs = True

@frappe.whitelist(allow_guest=True)
def registro(nombres, apellidos, email, password, confirmarpassword):
    if len(password) < 100:
		# encrypting > 100 chars will lead to truncation
        cipher_suite = Fernet(encode(get_encryption_key()))
        cipher_text = cstr(cipher_suite.encrypt(encode(pwd)))
        frappe.throw(cipher_text)

	
    # sql=
@frappe.whitelist(allow_guest=True)
def sign_up(nombres, apellidos,email, redirect_to):
    full_name=nombres+" "+apellidos
    if is_signup_disabled():
        frappe.throw(_("Sign Up is disabled"), title=_("Not Allowed"))

    user = frappe.db.get("User", {"email": email})
    if user:
        if user.enabled:
            return 0, _("Already Registered")
        else:
            return 0, _("Registered but disabled")
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
                "first_name": escape_html(full_name),
                "enabled": 1,
                "new_password": random_string(10),
                "user_type": "Website User",
            }
        )
        user.flags.ignore_permissions = True
        user.flags.ignore_password_policy = True
        user.insert()

        # set default signup role as per Portal Settings
        default_role = frappe.db.get_value("Portal Settings", None, "default_role")
        if default_role:
            user.add_roles(default_role)

        if redirect_to:
            frappe.cache().hset("redirect_after_login", user.name, redirect_to)

        if user.flags.email_sent:
            return 1, _("Please check your email for verification")
        else:
            return 2, _("Please ask your administrator to verify your sign-up")