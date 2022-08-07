// Copyright (c) 2022, Carolina Fonseca and contributors
// For license information, please see license.txt

frappe.ui.form.on('Datos Generales', {
	refresh: function(frm) {
		var now = moment();
        var total_days = moment(now).diff(frm.doc.fecha_nacimiento, "days");
        var edadcalculada = Math.floor((total_days).toFixed(2) / 365.25);
        frm.set_value('edad',edadcalculada);
        cur_frm.refresh_field(frm.doc.edad)
	}
});
