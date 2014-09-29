# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2012 Pexego Sistemas Informáticos All Rights Reserved
#    $Marta Vázquez Rodríguez$ <marta@pexego.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
        "name" : "Boardings Management",
        "version" : "1.0",
        "author" : "Pexego",
        "website" : "http://www.pexego.es",
        "category" : "Specific Industry Applications",
        "description": """Boardings Management in Openerp""",
        "depends" : ['base','report_aeroo','report_aeroo_ooo'],
        "init_xml" : [],
        "demo_xml" : [],
        "update_xml" : [
                        "security/boardings_management_security.xml",
                        "boat_view.xml",
                        "departures_view.xml",
                        "port_view.xml",
                        "situation_types_view.xml",
                        "vehicle_view.xml",
                        "identificative_document_view.xml",
                        "boardings_management_reports.xml",
                        "import_data/excel_treatment_view.xml",
                        "boardings_management_menu.xml",
                        "security/ir.model.access.csv",
                        "wizard/mult_records_management_wzd_view.xml",
                        "wizard/dua_summary_wizard_view.xml",
                        "boardings_management_wizard.xml",
                        ],
        "installable": True,
        'active': False

}
