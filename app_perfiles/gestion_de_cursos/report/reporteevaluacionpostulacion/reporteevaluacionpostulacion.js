function aprobar(codigo){
    
    frappe.confirm('¿Esta seguro de continuar con la aprobación del Pase?',
    () => {
        frappe.call({
            method: "app_perfiles.gestion_de_cursos.report.reporteevaluacionpostulacion.reporteevaluacionpostulacion.Aprobar",
            args: {
                codigo: codigo,
            },
            callback: (r) => {
                /*frappe.msgprint({
                   title: __('Notification'),
                   indicator: 'green',
                   message: r.message
                 });		 	*/
                 if (r.message == 1)
                 frappe.set_route("Form", "ApovadosXEvaluacion", codigo);
               },
        });
    }, () => {
        // action to perform if No is selected
    })
}