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
class document_type(osv.osv):

    _name = 'document.type'
    _description = 'Document type'
    _columns = {
        'name': fields.char('Definition', size=255, required=True)
    }

document_type()


class packaging_type(osv.osv):

    _name = "packaging.type"
    _columns = {
        'name': fields.char('Abbreviation', size=32, required=True),
        'description': fields.char('Description', size=255)
    }

packaging_type()

class identificative_document(osv.osv):

    _name = 'identificative.document'
    _description = 'Identificative document'
    _order = 'arrival_date desc, boarding_date desc'

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
        'name': fields.char('Document', size=32, required=True),
        'date': fields.date('Date'),
        'arrival_date': fields.date('Arrival date'),
        'boarding_date': fields.date('Boarding date'),
        'doc_type_id': fields.many2one('document.type', 'Type'),
        'ou_port_id': fields.many2one('ou.port', 'Org. Unit Port'),
        'veh_type_id': fields.many2one('vehicle.type', 'Vehicle type'),
        'dep_type_id': fields.many2one('departure.type', 'Departure type'),
        'weight': fields.float('Weight', digits=(16,2)),
        'boat_id': fields.many2one('boat', 'Boat'),
        'situation_id': fields.many2one('situation.types', 'Boarding situation'),
        'trademark': fields.char('Trademark', size=64),
        'model': fields.char('Model', size=64),
        'packaging': fields.many2one('packaging.type', 'Packaging'),
        'port_id': fields.many2one('port', 'Port'),
        'chassis': fields.char('Chassis', size=50),
        'measures': fields.char('Measures', size=50),
        'observations': fields.text('Observations'),
        'document': fields.char('Document Number', size=50),
        'units': fields.integer('Units'),
        'ou_port_ids_str': fields.function(_get_ou_port_ids_str, method=True, string='Ou port str', type='char', size=255),

    }
    _defaults={
        'units': lambda *a:1,
        'situation_id': lambda self, cr, uid, context: \
                        self.pool.get('situation.types').search(cr, uid, \
                                                        [('name','like', 'No embarcado')], context=context)\
                        and self.pool.get('situation.types').search(cr, uid, \
                                                        [('name','like', 'No embarcado')], context=context)[0]\
                        or False
    }

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

    def create(self, cr, uid, values, context=None):
        if values.get('ou_port_id',False):
                ou_port = self.pool.get('ou.port').browse(cr, uid, values['ou_port_id'])      
                if ou_port.port_id:
                    values.update({'port_id' : ou_port.port_id.id})
        return super(identificative_document, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        for doc in self.pool.get('identificative.document').browse(cr,uid,ids):
            if values.get('ou_port_id',False):
                ou_port = self.pool.get('ou.port').browse(cr, uid, values['ou_port_id'])      
                if ou_port.port_id:
                    values.update({'port_id' : ou_port.port_id.id})
        return super(identificative_document, self).write(cr, uid, ids, values, context=context)

identificative_document()
