import frappe

def get_permission_query_conditions_datos_generales(user):
    if not user: user = frappe.session.user
    if 'System Manager' in frappe.get_roles(user):
        return ""
    else:
        postulanteuser = frappe.defaults.get_user_default('postulanteuser')
        #clubuser = frappe.defaults.get_user_default('clubuser')
        if postulanteuser:# and not clubuser:
            return """(tabDatos Generales.name = '{0}')""".format(postulanteuser)
        #else:
        #    return """(tabClub.liga = '{0}' and  name = '{1}')""".format(ligauser, clubuser)

def get_permission_query_conditions_club(user):
    if not user: user = frappe.session.user
    if 'System Manager' in frappe.get_roles(user):
        return ""
    else:
        ligauser = frappe.defaults.get_user_default('ligauser')
        clubuser = frappe.defaults.get_user_default('clubuser')
        if ligauser and not clubuser:
            return """(tabClub.liga = '{0}')""".format(ligauser)
        else:
            return """(tabClub.liga = '{0}' and  name = '{1}')""".format(ligauser, clubuser)

def get_permission_query_conditions_liga(user):
    if not user: user = frappe.session.user
    if 'System Manager' in frappe.get_roles(user):
        return ""
    else:
        ligauser = frappe.defaults.get_user_default('ligauser')       
        if ligauser    :
            return """(tabLiga.name = '{0}')""".format(ligauser)


def get_permission_query_conditions_jugador(user):
    if not user: user = frappe.session.user
    if 'System Manager' in frappe.get_roles(user):
        return ""
    else:
        ligauser = frappe.defaults.get_user_default('ligauser')
        clubuser = frappe.defaults.get_user_default('clubuser')       
        if ligauser:
            if clubuser:
                return """(tabJugador.club  = '{0}' and tabJugador.liga = '{1}')""".format(clubuser ,ligauser )
            else:
                return """(tabJugador.liga = '{0}')""".format(ligauser)


def get_permission_query_conditions_clubjugadores(user):
    if not user: user = frappe.session.user
    if 'System Manager' in frappe.get_roles(user):
        return ""
    else:
        ligauser = frappe.defaults.get_user_default('ligauser')
        clubuser = frappe.defaults.get_user_default('clubuser')  
        if ligauser:
            if clubuser:                            
                return """(tabClubJugadores.club='{0}')""".format(clubuser )
            else:                 
                 return """(tabClubJugadores.liga='{0}')""".format(ligauser)
 

def get_permission_query_conditions_campeonato_categorias(user):
    if not user: user = frappe.session.user
    if 'System Manager' in frappe.get_roles(user):
        return ""
    else:
        ligauser = frappe.defaults.get_user_default('ligauser')
        clubuser = frappe.defaults.get_user_default('clubuser')
        if ligauser:
            if clubuser:
                return """(tabcampeonato_categorias.liga = '{0}')""".format(ligauser)
            else:
                return """(tabcampeonato_categorias.liga = '{0}')""".format(ligauser)
        