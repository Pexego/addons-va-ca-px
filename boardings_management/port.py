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

class port(osv.osv):

    _name = 'port'
    _description = 'Port'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'country_id': fields.many2one('res.country', 'Country', required=True),
    }

port()

class ou_port(osv.osv):

    _name = 'ou.port'
    _description = 'Organizational Unit of the Port'
    _columns = {
        'name': fields.char('Denomination', size=64, required=True),
        'port_id': fields.many2one('port', 'Port')
    }
    
ou_port()
