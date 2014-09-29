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

from report import report_sxw
from report.report_sxw import rml_parse

class Parser(report_sxw.rml_parse):
	"""Parser para publicar los campos del dua_summary_wizard"""
	def __init__(self, cr, uid, name, context):
		# import ipdb; ipdb.set_trace()
		super(Parser, self).__init__(cr,uid,name,context)
		self.localcontext.update({
			'get_out_port':self._get_out_port,
			'get_travel':self._get_travel,
			'get_code':self._get_code,
			})

	def _get_out_port(self):
		return self.localcontext['data']['form']['out_port']

	def _get_travel(self):
		return self.localcontext['data']['form']['travel']

	def _get_code(self):
		return self.localcontext['data']['form']['code']

