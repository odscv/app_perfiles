// Copyright (c) 2022, Carolina Fonseca and contributors
// For license information, please see license.txt

frappe.ui.form.on('AsignarCursoTecnico', {
	refresh: function(frm) {
		if(frappe.user.has_role("Postulante")){
            frm.set_df_property("tecnico", "hidden", 1);
            frm.set_df_property("nombre_tecnico", "hidden", 1);
	    }
	}
});
