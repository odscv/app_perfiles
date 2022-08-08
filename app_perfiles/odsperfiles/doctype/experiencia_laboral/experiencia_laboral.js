// Copyright (c) 2022, Carolina Fonseca and contributors
// For license information, please see license.txt

frappe.ui.form.on('Experiencia Laboral', {
	refresh: function(frm) {
		frm.set_value('meses', monthDiff(frm.doc.fecha_ingreso,frm.doc.fecha_salida));
		cur_frm.refresh_field(frm.doc.meses)
	}
});

function monthDiff(d1, d2) {
	d1 = new Date(d1);
	d2 = new Date(d2);
    var months;
    months = (d2.getFullYear() - d1.getFullYear()) * 12;
    months -= d1.getMonth();
    months += d2.getMonth();
    return months <= 0 ? 0 : months;
}