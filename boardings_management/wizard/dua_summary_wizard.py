# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2012 Pexego Sistemas Informáticos All Rights Reserved
#    $Javier Colmenero Fernández$ <javier@pexego.es>
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

from osv import osv, fields

class dua_summary_wizard(osv.osv_memory):

    _name = 'dua.summary.wizard'

    _columns = {
        # 'boarding_date': fields.date('Boarding date'),
        # 'boat_id': fields.many2one('boat', 'Boat'),
        'out_port': fields.char('Out Port', size=50),
        'travel': fields.char('Travel', size=50),
        'code': fields.char('Code', size=50),
    }

    def print_dua_summary(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        # import ipdb; ipdb.set_trace()
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model','identificative.document')
        data['form'] = self.read(cr,uid,ids[0],['out_port','travel','code'])

        return {'type': 'ir.actions.report.xml',
                'report_name': 'resumen_dua',
                'datas': data,
                }

    def print_manifiest(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        # import ipdb; ipdb.set_trace()
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model','identificative.document')
        data['form'] = self.read(cr,uid,ids[0],['out_port','travel','code'])

        return {'type': 'ir.actions.report.xml',
                'report_name': 'manifiesto_report',
                'datas': data,
                }
dua_summary_wizard()