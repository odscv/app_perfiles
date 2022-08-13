// Copyright (c) 2022, Carolina Fonseca and contributors
// For license information, please see license.txt

frappe.ui.form.on('Postulaciones', {
    refresh: function(frm) {
        //console.log(user_roles);
		if(frappe.user.has_role("Administrador Postulaciones")){
            frm.set_df_property("fase1", "read_only", 1);
            frm.set_df_property("puntaje_eval", "read_only", 0);
            console.log(frappe.user.has_role("Administrador Postulaciones"));
            /*if(frm.doc.aprobado==1){
                frm.set_df_property("direccion", "read_only", 1);
                frm.set_df_property("copia_cedula", "read_only", 1);
                frm.set_df_property("carnet_vacunacion", "read_only", 1);
            }*/
	    }
        console.log(frappe.user.has_role("TECNICO"));
		if(frappe.user.has_role("TECNICO")){
            frm.set_df_property("fase2", "read_only", 1);
            frm.set_df_property("puntaje_ent", "read_only", 0);
            console.log(frappe.user.has_role("Tecnicos"));
            /*if(frm.doc.aprobado==1){
                frm.set_df_property("direccion", "read_only", 1);
                frm.set_df_property("copia_cedula", "read_only", 1);
                frm.set_df_property("carnet_vacunacion", "read_only", 1);
            }*/
	    }
        if(frappe.user.has_role("Postulaciones")){
            frm.set_df_property("fase2", "read_only", 1);
            frm.set_df_property("puntaje_ent", "read_only", 1);
            frm.set_df_property("fase1", "read_only", 1);
            frm.set_df_property("puntaje_eval", "read_only", 1);
			if(frm.doc.putaje_ent)
            console.log(frm.doc.fase1);
            /*if(frm.doc.aprobado==1){
                frm.set_df_property("direccion", "read_only", 1);
                frm.set_df_property("copia_cedula", "read_only", 1);
                frm.set_df_property("carnet_vacunacion", "read_only", 1);
            }*/
	    }
	},
    puntaje_eval(frm) {

        frappe.call({
            method: "app_perfiles.api.get_puntaje_min",
            //freeze: true,
            args: {
                "codigo": frm.doc.codigocurso,
            }
        }).done((cal)=>{
            if(frm.doc.puntaje_eval>=cal.message[0].puntaje_min_evaluacion){
                cur_frm.set_value("fase1", 1);
            }else{
                cur_frm.set_value("fase1", 0);
            }
            cur_frm.refresh_field();
        });
	},
    puntaje_ent(frm) {

        frappe.call({
            method: "app_perfiles.api.get_puntaje_min",
            //freeze: true,
            args: {
                "codigo": frm.doc.codigocurso,
            }
        }).done((cal)=>{
            if(frm.doc.puntaje_ent>=cal.message[0].puntaje_min_entrevista){
                cur_frm.set_value("fase2", 1);
                let suma_puntaje = frm.doc.puntaje_ent + frm.doc.puntaje_eval;
                cur_frm.set_value("puntaje_total", suma_puntaje);
            }else{
                cur_frm.set_value("fase2", 0);
            }
            cur_frm.refresh_field();
        });
	},
});
