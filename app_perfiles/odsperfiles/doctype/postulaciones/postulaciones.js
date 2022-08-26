// Copyright (c) 2022, Carolina Fonseca and contributors
// For license information, please see license.txt

frappe.ui.form.on('Postulaciones', {
    refresh: function(frm) {
        //console.log(user_roles);
		if(frappe.user.has_role("Administrador Postulaciones")){
            frm.set_df_property("fase1", "read_only", 1);
            frm.set_df_property("puntaje_eval", "read_only", 0);
            frm.set_df_property("fase2", "read_only", 1);
            
            
	    }
		if(frappe.user.has_role("TECNICO")){
            frm.set_df_property("fase2", "read_only", 1);
            frm.set_df_property("id_participante", "read_only", 1);
            frm.set_df_property("codigocurso", "read_only", 1);
            frm.set_df_property("puntaje_ent", "read_only", 0);
	    }
        if(frappe.user.has_role("Postulante")){
            frm.set_df_property("fase2", "read_only", 1);
            frm.set_df_property("puntaje_ent", "hidden", 1);
            frm.set_df_property("fase1", "read_only", 1);
            frm.set_df_property("puntaje_eval", "hidden", 1);
            frm.set_df_property("puntaje_total", "read_only", 0);
            frm.set_df_property("puntaje_total", "hidden", 0);
	    }
        cur_frm.refresh_field();
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
            if(frm.doc.fase1 && frm.doc.fase2){
                
                cur_frm.set_value("resultado", "Aprobado(a)");
            }else{
                cur_frm.set_value("resultado", "No Aprobado(a)");
            }
            let suma_puntaje = frm.doc.puntaje_ent + frm.doc.puntaje_eval;
            cur_frm.set_value("puntaje_total", suma_puntaje);
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
            console.log(cal.message[0].puntaje_min_entrevista);
            if(frm.doc.puntaje_ent>=cal.message[0].puntaje_min_entrevista){
                cur_frm.set_value("fase2", 1);
            }else{
                cur_frm.set_value("fase2", 0);
            }
            if(frm.doc.fase1 && frm.doc.fase2){
                
                cur_frm.set_value("resultado", "Aprobado(a)");
            }else{
                cur_frm.set_value("resultado", "No Aprobado(a)");
            }
            
                //cur_frm.set_value("resultado", "Reprobado");
            let suma_puntaje = frm.doc.puntaje_ent + frm.doc.puntaje_eval;
            cur_frm.set_value("puntaje_total", suma_puntaje);
            cur_frm.refresh_field();
        });
	},
});
