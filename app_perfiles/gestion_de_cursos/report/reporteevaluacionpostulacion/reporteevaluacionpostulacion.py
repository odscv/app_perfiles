import frappe

@frappe.whitelist()
def Aprobar(codigo):
    pal = frappe.get_doc("Postulaciones",codigo)
    ent = frappe.new_doc("ApovadosXEvaluacion")
    ent.id_participante = pal.id_participante
    ent.nombres_el = pal.nombres_el
    ent.codigocurso = pal.codigocurso
    ent.curso = pal.curso
    #frappe.throw(ent.curso)
    ent.insert()
    msg ="""Se ha Geneardo el registro, para completar la aprobación, debe validar el documento:  <a href="/app/apovadosxevaluacion/{0}">{0}</a>  """.format(ent.name)
    return 1
    