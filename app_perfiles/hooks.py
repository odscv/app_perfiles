from . import __version__ as app_version

app_name = "app_perfiles"
app_title = "Perfiles ODSCV"
app_publisher = "Carolina Fonseca"
app_description = "Aplicacion para administrar postulaciones ."
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "caro-fonseca@outlook.com"
app_license = "MIT"

# Includes in <head>
# ------------------
on_session_creation = [
	#"app_perfiles.odsperfiles.doctype.postulaciones.postulaciones.setdatosg"
	"app_perfiles.odsperfiles.doctype.datos_generales.datos_generales.setdatosg"
]

# include js, css files in header of desk.html
# app_include_css = "/assets/app_perfiles/css/app_perfiles.css"
# app_include_js = "/assets/app_perfiles/js/app_perfiles.js"

# include js, css files in header of web template
# web_include_css = "/assets/app_perfiles/css/app_perfiles.css"
# web_include_js = "/assets/app_perfiles/js/app_perfiles.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "app_perfiles/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "app_perfiles.install.before_install"
# after_install = "app_perfiles.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "app_perfiles.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
permission_query_conditions = {
	"Datos Generales": "app_perfiles.filtros.filtros.get_permission_query_conditions_datos_generales",	 
	#"Liga": "kopa.filtros.filtros.get_permission_query_conditions_liga",
	#"Jugador": "kopa.filtros.filtros.get_permission_query_conditions_jugador",
	#"ClubJugadores": "kopa.filtros.filtros.get_permission_query_conditions_clubjugadores",
	#"campeonato_categorias": "kopa.filtros.filtros.get_permission_query_conditions_campeonato_categorias",
}

# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"app_perfiles.tasks.all"
# 	],
# 	"daily": [
# 		"app_perfiles.tasks.daily"
# 	],
# 	"hourly": [
# 		"app_perfiles.tasks.hourly"
# 	],
# 	"weekly": [
# 		"app_perfiles.tasks.weekly"
# 	]
# 	"monthly": [
# 		"app_perfiles.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "app_perfiles.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "app_perfiles.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "app_perfiles.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"app_perfiles.auth.validate"
# ]

