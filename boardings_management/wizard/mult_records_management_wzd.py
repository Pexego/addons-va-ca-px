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

from osv import osv, fields

class multi_records_management(osv.osv_memory):

    _name = 'multi.records.management'

    def _get_ou_port_ids_str(self, cr, uid, ids, field_name, args, context=None):

        res = {}
        for doc in self.browse(cr, uid, ids):
            res[doc.id] = ""
            stream = []
            if doc.port_id:
                stream.append(str(doc.port_id.id))
                res[doc.id] = u"/".join(stream)

        return res

    _columns = {
        'boarding_date': fields.date('Boarding date'),
        'boat_id': fields.many2one('boat', 'Boat'),
        'port_id': fields.many2one('port', 'Port'),
        'ou_port_id': fields.many2one('ou.port', 'Org. Unit Port'),
        'dep_type_id': fields.many2one('departure.type', 'Departure type'),
        'situation_id': fields.many2one('situation.types', 'Boarding situation'),
        'doc_ids_str': fields.char('Doc ids', size=255, readonly=True),
        'ou_port_ids_str': fields.function(_get_ou_port_ids_str, method=True, string='Ou port str', type='char', size=255),
    }

    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        
        res = {}

        if not context.get('active_ids', []) or not context.get('active_model') == 'identificative.document':
            return res
        stream = []
        for x in context['active_ids']:
            stream.append(str(x))

        res['doc_ids_str'] = u"/".join(stream)

        return res
    def onchange_port_id(self, cr, uid, ids, port_id, context=None):
        """
            Fills the port field with the port that belongs to the
            Organizational Unit of the Port selected
        """
        if port_id:
            stream = []
            stream.append(str(port_id))
            return {'value': {'ou_port_ids_str': u"/".join(stream)}}
        return {}

    def update_docs(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        doc = self.pool.get('identificative.document')

        for cur in self.browse(cr, uid, ids, context):
            if cur.doc_ids_str:
                for x in (cur.doc_ids_str).split('/'):
                    id = int(x)
                    if cur.boarding_date:
                        doc.write(cr, uid, [id], {'boarding_date': cur.boarding_date})
                    if cur.boat_id:
                        doc.write(cr, uid, [id], {'boat_id': cur.boat_id.id})
                    if cur.port_id:
                        doc.write(cr, uid, [id], {'port_id': cur.port_id.id})
                    if cur.ou_port_id:
                        doc.write(cr, uid, [id], {'ou_port_id': cur.ou_port_id.id})
                    if cur.dep_type_id:
                        doc.write(cr, uid, [id], {'dep_type_id': cur.dep_type_id.id})
                    if cur.situation_id:
                        doc.write(cr, uid, [id], {'situation_id': cur.situation_id.id})

        return {'type': 'ir.actions.act_window_close'}


multi_records_management()




