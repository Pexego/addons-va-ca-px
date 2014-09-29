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
import base64
import logging
import xlrd
import time
from time import gmtime, strftime
from datetime import datetime
import StringIO
import tools

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def _get_alfabet(self, cr, uid, context=None):
        cCols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numero = 25
        ###Incrementamos uno a la variable numero, para sacar el ultimo par que es el '26', 'Z'.
        #_logger.debug('_get_alfabet: ' + str([(str(r), cCols[r:r+1]) for r in range(numero+1)]))
        return [(str(r), cCols[r:r+1]) for r in range(numero+1)]

def _get_number(self, cr, uid, context=None):
        numero = 39
        ### Como las Filas son N-1, hay que quitar uno a la Fila que indique la parametrizacion,
        ### ya que si no dejaremos la primera fila sin leer. Por eso se queda en R la fila y la columna
        ###Incrementamos uno a la variable numero, para sacar el ultimo par que es el '40', '40'.
        #_logger.debug('_get_number: ' + str([(str(r), str(r+1)) for r in range(numero+1)]))
        return [(str(r), str(r+1)) for r in range(numero+1)]

def colindx(coln):
        """ 7 => 'H', 27 => 'AB' """
        indice = -1
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if len(coln)<=1:
                try:
                        indice = alphabet.index(coln)
                except ValueError:
                        indice = -2 ###'No encontrada'
        else:
                indice = -2 ###'No encontrada'
        return indice

def dvce(workbook, worksheet, curr_row, cell_ind):
        cell_type = ""
        cell_value = ""
        if cell_ind >= 0:
                ### Hay que controlar el error ya que puede seleccionar una columna que no este
                ### instanciada en el excel, y esto hace que ya no haya mas lecturas. Es por ello que
                ### procederemos a poner en blanco la celda y haremos una ruptura en la funcion.
                try:
                        cell_type = worksheet.cell_type(curr_row, cell_ind)
                except:
                        cell_value = ""
                        return cell_value

                ### Hay que controlar el tipo de dato
                if cell_type == xlrd.XL_CELL_EMPTY:
                        cell_value = ""
                elif cell_type == xlrd.XL_CELL_TEXT:
                        cell_value = worksheet.cell_value(curr_row, cell_ind)
                elif cell_type == xlrd.XL_CELL_NUMBER:
                        cell_value = float(worksheet.cell_value(curr_row, cell_ind))
                elif cell_type == xlrd.XL_CELL_DATE:
                        ### Extraemos los datos en forma de TUPLE
                        cTmp = xlrd.xldate_as_tuple(worksheet.cell_value(curr_row, cell_ind), workbook.datemode)
                        ### Al TUPLE hay que anadirle elementos hasta llegar a 9, ya que la Fecha
                        ### en Excel es un TUPLE de 6, y en PYTHON es necesario que sea de 9.
                        if len(cTmp) < 9:
                                for i in range (len(cTmp),9):
                                        cTmp += (0,)
                        cTmp = time.mktime(cTmp)
                        cell_value = time.strftime("%d/%m/%Y", time.gmtime(cTmp))
                elif cell_type == xlrd.XL_CELL_BOOLEAN:
                        cell_value = bool(worksheet.cell_value(curr_row, cell_ind))
                else:
                        cell_value = worksheet.cell_value(curr_row, cell_ind)
        #_logger.debug('cell_value: ' + str(cell_value) + ' - curr_row: ' + str(curr_row) + ' - cell_ind: ' + str(cell_ind))
        return cell_value

class excel_upload(osv.osv):
        """Gestion de Excel - Upload""" ###, filters = '*.xlsx, *.xls'
        _name = 'excel.upload'
        _columns = {
                'idUsr': fields.char('idUsr',size=18, help='Usuario'),
                'FechaCarga': fields.char('FechaCarga',size=14, help="Fecha de carga", readonly=False),
                'ficheroUp': fields.binary('File', required="True", filters = '*.xls,*.xlsx,*.XLS,*.XLSX,*.Xls,*.Xlsx'),
                'hoja' : fields.char('Hoja del libro en la que debe hacerse la lectura', help="Hoja del libro en la que debe hacerse la lectura", type="char", size=128, readonly=False, required=True),
                'filaIni' : fields.integer('Fila en la que se comienza la Lectura',required=True, readonly=False),
                'filaFin' : fields.integer('Fila en la que finaliza la Lectura', readonly=False),
                'colFechaLlegada' : fields.selection(_get_alfabet,'Columna Fecha de Llegada', size=3, readonly=False),
                'colDocumento': fields.selection(_get_alfabet,'Columna Documento', size=3, required=True, readonly=False),
                'colFechaDocumento':fields.selection(_get_alfabet,'Fecha de Documento', size=3, readonly=False),
                'colNumerodocumento': fields.selection(_get_alfabet,'Columna Tipo Documento', size=3, readonly=False),
                'colSituacionEmbarque': fields.selection(_get_alfabet,'Columna Situacion Embarque', size=3, readonly=False),
                'colMarca': fields.selection(_get_alfabet,'Columna Marca', size=3, readonly=False),
                'colModelo': fields.selection(_get_alfabet,'Columna Modelo', size=3, readonly=False),
                'colCar': fields.selection(_get_alfabet,'Columna CAR', size=3, readonly=False),
                'colPU': fields.selection(_get_alfabet,'Columna PU', size=3, readonly=False),
                'colHH': fields.selection(_get_alfabet,'Columna HH', size=3, readonly=False),
                'colSTC': fields.selection(_get_alfabet,'Columna STC', size=3, readonly=False),
                'colEmbalaje': fields.selection(_get_alfabet,'Columna Embalaje', size=3, readonly=False),
                'colPartida': fields.selection(_get_alfabet,'Columna Partida', size=3, readonly=False),
                'colPeso': fields.selection(_get_alfabet,'Columna Peso', size=3, readonly=False),
                'colUOport': fields.selection(_get_alfabet, 'Columna U. Org. Puerto', size=3, readonly=False),
                'colChasis': fields.selection(_get_alfabet, 'Columna Chasis', size=3, readonly=False, required=True),
                'colMedidas': fields.selection(_get_alfabet, 'Columna Medidas', size=3, readonly=False)
        }

        _defaults = {
                'idUsr': lambda self, cr, uid, context: uid,
                'FechaCarga': lambda *a: strftime('%Y%m%d%H%M%S'),
                'hoja': 'Hoja 1',
        }

        def import_file(self, cr, uid, ids, vals, context=None):
            if context is None:
                    context = {}
            new_ids = []
            impo = self.browse(cr, uid, ids[0])

            ficheroUp = impo.ficheroUp
            hoja = impo.hoja
            filaIni = impo.filaIni
            filaFin = impo.filaFin
            colUOport = impo.colUOport
            colFechaLlegada = impo.colFechaLlegada
            colDocumento = impo.colDocumento
            colFechaDocumento = impo.colFechaDocumento
            colNumerodocumento = impo.colNumerodocumento
            colSituacionEmbarque = impo.colSituacionEmbarque
            colChasis = impo.colChasis
            colMarca = impo.colMarca
            colModelo = impo.colModelo
            colCar = impo.colCar
            colPU = impo.colPU
            colHH = impo.colHH
            colSTC = impo.colSTC
            colEmbalaje = impo.colEmbalaje
            colPartida = impo.colPartida
            colPeso = impo.colPeso
            colMedidas = impo.colMedidas

            if len(ficheroUp)<1:
                raise osv.except_osv('Warning!','Debe seleccionar al menos un archivo para poder importar! Seleccione un fichero.')

            if len(hoja)<1:
                raise osv.except_osv('Warning!','Debe introducir un nombre de Hoja Excel!','Introducir Nombre de Hoja.')

            if len(colDocumento)<1:
                raise osv.except_osv('Warning!','Debe introducir al menos la ubicacion de la columna del Documento de Embarque! Introducir Columna Documento.')

            ### Realizamos el tratamiento del Excel.
            try:
                file = base64.b64decode(ficheroUp)
                workbook = xlrd.open_workbook(file_contents=StringIO.StringIO(file).read(), encoding_override="utf-8")
            except:
                raise osv.except_osv('Warning!','El archivo que ha subido no es un fichero compatible con Microsoft Excel o es erroneo! Verifique que sea un fichero Excel.')

            try:
                worksheet = workbook.sheet_by_name(hoja)
            except:
                worksheet = None

            ### Si worksheet == None, quiere decir que el nombre de la hoja no existe,
            ### por consiguiente no se puede seguir realizando la importacion
            if worksheet == None:
                raise osv.except_osv('Warning!','La Hoja '+ hoja + ' no existe o ha introducido mal su nombre! Verifique el nombre de la hoja.')

            num_rows = worksheet.nrows - 1
            curr_row = int(filaIni) - 1 
            end_row = filaFin and int(filaFin) -1  or num_rows
            # import ipdb; ipdb.set_trace()
            ### Recorremos todas las filas de la Hoja Excel
            while curr_row <= end_row:
                ### Variables de Registro
                sUOport = ""
                sFechaLlegada = ""
                sDocumento = ""
                sFechaDocumento = ""
                sNumerodocumento = ""
                sSituacionEmbarque = ""
                sChasis = ""
                sMarca = ""
                sModelo = ""
                sCar = ""
                sPU = ""
                sHH = ""
                sSTC = ""
                sEmbalaje = ""
                sPartida = ""
                sPeso = ""
                sMedidas = ""
                vehicle = []
                ouport = []
                situation = []
                packaging = []
                dep_type_id = []

                document_data = {}
                if colUOport:
                    sUOport = dvce(workbook, worksheet, curr_row, int(colUOport))
                    ouport = self.pool.get('ou.port').search(cr, uid, [('name', '=', sUOport)])
                    if not ouport:
                        raise osv.except_osv('Warning!','La Uni. Org. de Puerto '+ sUOport + ' no existe o ha introducido mal su nombre!')
                    document_data.update({'ou_port_id' : ouport[0]})

                if int(colFechaLlegada):
                    sFechaLlegada = dvce(workbook, worksheet, curr_row, int(colFechaLlegada))
                    if not sFechaLlegada:
                        raise osv.except_osv('Warning!','El campo Fecha de LLegada está vacío!')
                    document_data.update({'arrival_date' : sFechaLlegada})
                if int(colDocumento):
                    sDocumento = dvce(workbook, worksheet, curr_row, int(colDocumento))

                    if sDocumento == "" or sDocumento == None:
                        raise osv.except_osv('Warning!','Columna DOCUMENTO Obligatoria, debe estar cumplimentada en el fichero EXCEL! \nPor favor, revísela!')
                    if type(sDocumento) == float:
                        document_data.update({'name' : str(int(sDocumento))})
                    else:
                        document_data.update({'name' : str(sDocumento)})

                if int(colFechaDocumento):
                    sFechaDocumento = dvce(workbook, worksheet, curr_row, int(colFechaDocumento))
                    if not sFechaDocumento:
                        raise osv.except_osv('Warning!','El campo Fecha de Documento está vacío!')
                    document_data.update({'date' : sFechaDocumento})

                if int(colNumerodocumento):
                    sNumerodocumento = dvce(workbook, worksheet, curr_row, int(colNumerodocumento))
                    if not sNumerodocumento:
                        raise osv.except_osv('Warning!','Columna TIPO DOCUMENTO Obligatoria, debe estar cumplimentada en el fichero EXCEL! \nPor favor, revísela!')
                    if type(sNumerodocumento) == float:
                        document_data.update({'document' : str(int(sNumerodocumento))})
                    else:
                        document_data.update({'document' : str(sNumerodocumento)})

                if int(colSituacionEmbarque):
                    sSituacionEmbarque = dvce(workbook, worksheet, curr_row, int(colSituacionEmbarque))
                    situation = self.pool.get('situation.types').search(cr, uid, [('name', '=', sSituacionEmbarque)])
                    document_data.update({'situation_id' : situation and situation[0] or False})

                if int(colChasis):
                    sChasis = dvce(workbook, worksheet, curr_row, int(colChasis))
                    if not sChasis:
                        raise osv.except_osv('Warning!','Columna CHASIS Obligatoria, debe estar cumplimentada en el fichero EXCEL! \nPor favor, revísela!')
                    if type(sChasis) == float:
                        document_data.update({'chassis' : str(int(sChasis))})
                    else:
                        document_data.update({'chassis' : str(sChasis)})

                if int(colMarca):
                    sMarca = dvce(workbook, worksheet, curr_row, int(colMarca))
                    if not sMarca:
                        raise osv.except_osv('Warning!','El campo Marca está vacío!')
                    document_data.update({'trademark' : sMarca})

                if int(colModelo):
                    sModelo = dvce(workbook, worksheet, curr_row, int(colModelo))
                    if not sModelo:
                        raise osv.except_osv('Warning!','El campo Modelo está vacío!')
                    document_data.update({'model' : sModelo })

                if int(colCar) or int(colPU) or int(colHH) or int(colSTC):
                    if int(colCar):
                        sCar = dvce(workbook, worksheet, curr_row, int(colCar))

                    if int(colPU):
                        sPU = dvce(workbook, worksheet, curr_row, int(colPU))

                    if int(colHH):
                        sHH = dvce(workbook, worksheet, curr_row, int(colHH))

                    if int(colSTC):
                        sSTC = dvce(workbook, worksheet, curr_row, int(colSTC))

                    if not sCar and not sPU and not sHH and not sSTC:
                        raise osv.except_osv('Warning!','Al menos uno de los campos CAR, P/U, H/H o STC debe estar marcado')
                    else:

                        if sCar:
                            vehicle = self.pool.get('vehicle.type').search(cr, uid, [('name', 'like', 'CAR')])
                        elif sPU:
                            vehicle = self.pool.get('vehicle.type').search(cr, uid, [('name', 'like', 'P/U')])
                        elif sHH:
                            vehicle = self.pool.get('vehicle.type').search(cr, uid, [('name', 'like', 'H/H')])
                        elif sSTC:
                            vehicle = self.pool.get('vehicle.type').search(cr, uid, [('name', 'like', 'STC')])
                        document_data.update({'veh_type_id' : vehicle and vehicle[0] or False})

                if int(colEmbalaje):
                    sEmbalaje = dvce(workbook, worksheet, curr_row, int(colEmbalaje))
                    packaging = self.pool.get('packaging.type').search(cr, uid, [('name', 'like', sEmbalaje)])
                    if not packaging:
                        raise osv.except_osv('Warning!','El embalaje '+ sEmbalaje + ' no existe o ha introducido mal su nombre!')
                    document_data.update({'packaging': packaging and packaging[0] or False})

                if int(colPartida):
                    sPartida = dvce(workbook, worksheet, curr_row, int(colPartida))
                    dep_type_id = self.pool.get('departure.type').search(cr, uid, [('name', 'like', tools.ustr(sPartida))])
                    if not sPartida:
                        raise osv.except_osv('Warning!','El campo Partida está vacío!')
                    if not dep_type_id:
                        raise osv.except_osv('Warning!',u'La partida '+ tools.ustr(sPartida) + u' no existe o ha introducido mal su nombre!')
                    document_data.update({'dep_type_id': dep_type_id and dep_type_id[0] or False})

                if int(colPeso):
                    sPeso = dvce(workbook, worksheet, curr_row, int(colPeso))
                    if not sPeso:
                        raise osv.except_osv('Warning!','El campo Peso está vacío!')
                    document_data.update({'weight': sPeso and float(sPeso) or 0.0})
                if int(colMedidas):
                    sMedidas = dvce(workbook, worksheet, curr_row, int(colMedidas))
                    document_data.update({'medidas': sMedidas})

                update_ids = self.pool.get('identificative.document').search(cr,uid,[('name','=',document_data['name']),('chassis','=',document_data['chassis'])])
                if update_ids:
                    self.pool.get('identificative.document').write(cr,uid,update_ids,document_data, context=context)
                    new_ids = list(set(new_ids + update_ids))
                else:
                    new_id = self.pool.get('identificative.document').create(cr, uid, document_data, context=context)
                    new_ids.append(new_id)

                ### Pasamos a la siguiente fila
                curr_row += 1

            return {
                'name': 'Identificative Documents imported',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'identificative.document',
                'type': 'ir.actions.act_window',
                'domain': [('id','in', new_ids)],
                'nodestroy': True
            }
excel_upload()