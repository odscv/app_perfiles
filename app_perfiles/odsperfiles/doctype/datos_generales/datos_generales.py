# Copyright (c) 2022, Carolina Fonseca and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DatosGenerales(Document):
	def before_insert(self):
		self.nombrecompleto  = self.nombres + " " + self.apellidos
	
