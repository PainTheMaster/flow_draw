import openpyxl as xl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment, PatternFill, Font
from typing import List
import re
import flow_draw.definitions as defs
import math
import flow_draw.batch.process.unit_operations.uo_charging as chgng
from flow_draw.batch.process.unit_operations.uo_charging import Input
from flow_draw.trait_def.trait_def import GetInputs



line_thin = defs.xl_line_thin

border_left = defs.xl_border_left
border_right = defs.xl_border_right
border_top = defs.xl_border_top
border_bottom = defs.xl_border_bottom
border_around = defs.xl_border_around
alignment_center = defs.xl_alignment_center
alignment_left = defs.xl_alignment_left

"""
#A6C9EC (light blue)
#DAE9F8 (lighter blue)

#EFC1A7 (light orange)
#FBE2D5 (lighter orange)
"""
fill_light_blue = PatternFill(fgColor="A6C9EC", fill_type="solid")
fill_lighter_blue = PatternFill(fgColor="DAE9F8", fill_type="solid")
fill_light_orange = PatternFill(fgColor="EFC1A7", fill_type="solid")
fill_lighter_orange = PatternFill(fgColor="FBE2D5", fill_type="solid")

font_bold = Font(bold=True)


line_start = 1
#line_standard = line_start
line_xlslog_hedr = line_start

col_time = 1
col_op_nr = 2
col_title_left_half = 3
col_title_right_half =4
col_method = 4
col_content = 5
col_record = 6
col_operator = 7
col_witness = 8

col_xlslog_mat = 10
col_xlslog_mw = 11
col_xlslog_dens = 12
col_xlslog_assay_conc = 13

col_xlslog_name_basis = 14
col_xlslog_mol_basis = 15
col_xlslog_kg_net_basis = 16

col_xlslog_equiv = 17
col_xlslog_v_per_w = 18
col_xlslog_wwpct = 19
col_xlslog_wt_abs_kg_gro =20
col_xlslog_vol_abs =21

col_xlslog_mol = 22
col_xlslog_volume = 23
col_xlslog_kg_net = 24
col_xlslog_kg_gro = 25
col_xlslog_err_rel = 26
col_xlslog_err_abs = 27

# col_xlslog_name_basis = 23
# col_xlslog_id_basis = 24
# col_xlslog_class = 25
# col_xlslog_mol_std = 26
# col_xlslog_kg_net_std = 27





tag_part_hedr_mat = "tag_hedr_mat"
"""Tag for header material"""
tag_part_hedr_mw = "tag_hedr_mw"
"""Tag for header molecular weight"""
tag_part_hedr_dens = "tag_hedr_dens"
"""Tag for header density"""
tag_part_hedr_assay_conc = "tag_hedr_assay_conc"
"""Tag for header assay concentration"""
tag_part_hedr_name_basis = "tag_hedr_name_basis"
"""Tag for header name basis"""
tag_part_hedr_mol_basis = "tag_hedr_mol_basis"
"""Tag for header mol basis"""
tag_part_hedr_kg_net_basis = "tag_hedr_kg_net_basis"
"""Tag for header net weight basis"""
tag_part_hedr_equiv = "tag_hedr_equiv"
"""Tag for header equivalent"""
tag_part_hedr_v_per_w = "tag_hedr_v/w"
"""Tag for header volume per weight"""
tag_part_hedr_wwpct = "tag_hedr_wwpct"
"""Tag for header weight percent"""
tag_part_hedr_wt_gro_abs = 'tag_hedr_weight_kg_gro_abs'
"""Tag for header kg gross absolute"""
tag_part_hedr_vol_abs = 'tag_hedr_vol_abs'
"""Tag for header volume absolute"""
tag_part_hedr_mol = "tag_hedr_mol"
"""Tag for header mol"""
tag_part_hedr_volume = "tag_hedr_volume"
"""Tag for header volume"""
tag_part_hedr_kg_net = "tag_hedr_kg_net"
"""Tag for header net weight"""
tag_part_hedr_kg_gro = "tag_hedr_wt_kg_gro"
"""Tag for header gross weight""" 
tag_part_hedr_err_rel = "tag_hedr_err_rel"
"""Tag for header relative error"""
tag_part_hedr_err_abs = "tag_hedr_err_abs"
"""Tag for header absolute error"""
tag_part_hedr_basis_name = 'tag_name_basis'
"""Tag for the name of the basis material"""
tag_part_hedr_basis_id = 'tag_id_basis'
"""Tag for the ID of the basis material"""
tag_part_hedr_basis_class = 'tag_class_basis'
"""Tag for the class of the basis material"""
tag_part_hedr_basis_mol = 'tag_mol_basis'
"""Tag for standard mol value"""
tag_part_hedr_basis_wt_net = 'tag_wt_net_basis'
"""Tag for standard net weight value"""


dict_part_logic_jp ={tag_part_hedr_mat: "Material",
                     tag_part_hedr_mw: "MW(g/mol)",
                     tag_part_hedr_dens: "d(g/mL)",
                     tag_part_hedr_assay_conc: "Assay/Conc(%)",
                     tag_part_hedr_name_basis: "BasisComp",
                     tag_part_hedr_mol_basis: "Basis_n(mol)",
                     tag_part_hedr_kg_net_basis: "Basis_wt(kg-net)",
                     tag_part_hedr_equiv: "Equiv",
                     tag_part_hedr_v_per_w: "v/w",
                     tag_part_hedr_wwpct: "w/w%",
                     tag_part_hedr_wt_gro_abs:"Wt_abs(kg-gross)",
                     tag_part_hedr_vol_abs:'Vol_abs(L)',
                     tag_part_hedr_mol: "n(mol)",
                     tag_part_hedr_volume: "V(L)",
                     tag_part_hedr_kg_net: "Wt(kg-net)",
                     tag_part_hedr_kg_gro: "Wt(kg-gross)",
                     tag_part_hedr_err_rel: "Err(%)",
                     tag_part_hedr_err_abs: "Err(kg)",
                     tag_part_hedr_basis_name: "Material",
                     tag_part_hedr_basis_id: "ID_input",
                     tag_part_hedr_basis_class: "Class",
                     tag_part_hedr_basis_mol: "n(mol)",
                     tag_part_hedr_basis_wt_net: "Wt(kg-net)"}
dict_part_logic = dict_part_logic_jp

def num_to_alph(num_col:int)->str:
    if num_col <= 0:
        raise ValueError(f'Flowsheet.num_to_alpha(): Invalid "num_col"=={num_col}. This has to be a positive natural number')
    base=26
    code_A = ord('A')
    result = ''
    while num_col > 0:
        num_col -= 1
        result = chr(code_A+(num_col % base)) + result
        num_col //= base
    return result

alph_col_time = num_to_alph(num_col = col_time)
alph_col_op_nr = num_to_alph(num_col = col_op_nr)
alph_col_title_left_half = num_to_alph(num_col = col_title_left_half)
alph_col_title_right_half = num_to_alph(num_col = col_title_right_half)

alph_col_mat = num_to_alph(num_col = col_xlslog_mat)
alph_col_mw = num_to_alph(num_col = col_xlslog_mw)
alph_col_dens = num_to_alph(num_col = col_xlslog_dens)
alph_col_assay_conc = num_to_alph(num_col = col_xlslog_assay_conc)

alph_col_name_basis = num_to_alph(num_col = col_xlslog_name_basis)
alph_col_mol_basis = num_to_alph(num_col = col_xlslog_mol_basis)
alph_col_kg_net_basis = num_to_alph(num_col = col_xlslog_kg_net_basis)

alph_col_equiv = num_to_alph(num_col = col_xlslog_equiv)
alph_col_v_per_w = num_to_alph(num_col = col_xlslog_v_per_w)
alph_col_wwpct = num_to_alph(num_col = col_xlslog_wwpct)
alph_col_kg_gro_abs = num_to_alph(num_col=col_xlslog_wt_abs_kg_gro)
alph_col_vol_abs = num_to_alph(num_col=col_xlslog_vol_abs)

alph_col_mol = num_to_alph(num_col = col_xlslog_mol)
alph_col_volume = num_to_alph(num_col = col_xlslog_volume)
alph_col_kg_net = num_to_alph(num_col = col_xlslog_kg_net)
alph_col_kg_gro = num_to_alph(num_col = col_xlslog_kg_gro)
alph_col_err_rel = num_to_alph(num_col = col_xlslog_err_rel)
alph_col_err_abs = num_to_alph(num_col = col_xlslog_err_abs)


class Flowsheet:
    def __init__(self):
        self.wb = xl.Workbook()
        self.ws = self.wb.active
        self.current_line = line_start
        self.mol_std:float = 0.0
        self.wt_net_std:float = 0.0
        # self.dict_basis:dict{int, int} = {}

    def set_standards(self, mol_std: float=0.0, wt_net_std: float=0.0):
        self.mol_std = mol_std
        self.wt_net_std = wt_net_std

    def put_body_comments(self, comments :str):
        cmt_brkdwn = re.split('[\n;]', comments)
        self.body_organizer(list_col_time=[],
                            list_col_method=[],
                            list_col_content=cmt_brkdwn,
                            list_col_record=[],
                            list_col_operator=[],
                            list_col_witness=[])
        #self.linefeed()

    def header_organizer(self,
                         op_nr: int|str|None=None,
                         title: str=None)->int:
        self.ws.merge_cells(start_row=self.current_line, start_column=col_title_left_half, end_row=self.current_line, end_column=col_title_right_half)
        if isinstance(op_nr, int) or isinstance(op_nr, str):
            self.ws.cell(row=self.current_line, column=col_op_nr, value=op_nr)
        elif op_nr is None:
            cell_start = f'${alph_col_title_left_half}${line_start}'
            cell_this_line = f'{alph_col_title_left_half}{self.current_line}'
            xls_formular_count = f'=IF({cell_this_line}<>"", COUNTA({cell_start}:{cell_this_line}), "")'
            self.ws.cell(row=self.current_line, column=col_op_nr, value=xls_formular_count)
        self.ws.cell(row=self.current_line, column=col_title_left_half, value=title)
        self.ws.cell(row=self.current_line, column=col_op_nr).border = border_around
        self.ws.cell(row=self.current_line, column=col_op_nr).alignment = alignment_center
        self.ws.cell(row=self.current_line, column=col_title_left_half).border = Border(left=line_thin, top=line_thin, bottom=line_thin)
        self.ws.cell(row=self.current_line, column=col_title_right_half).border = Border(top=line_thin, bottom=line_thin, right=line_thin)
        self.ws.cell(row=self.current_line, column=col_title_left_half).alignment = alignment_center
        self.__put_excel_logic(line=self.current_line)

        self.current_line += 1
        return self.current_line-1

    def put_line(self, time: str ='', method: str='', content: str='', record: str='', operator: str='', witness: str='')->int:
        self.ws.cell(row=self.current_line, column=col_time).value = time
        self.ws.cell(row=self.current_line, column=col_method).value = method
        self.ws.cell(row=self.current_line, column=col_content).value = content
        self.ws.cell(row=self.current_line, column=col_record).value = record
        self.ws.cell(row=self.current_line, column=col_operator).value = operator
        self.ws.cell(row=self.current_line, column=col_witness).value = witness
        self.ws.cell(row=self.current_line, column=col_method).border = border_left
        self.__put_excel_logic(line=self.current_line)

        self.current_line += 1
        return self.current_line-1

    # def put_material(self,
    #                  time: str ='',
    #                  method: str='',
    #                  record: str='',
    #                  operator: str='',
    #                  witness: str='',
    #                  name_mat:str=None,
    #                  mw:float=None,
    #                  dens:float=None,
    #                  assay_conc:float=None,
    #                  equiv:float=None,
    #                  v_per_w:float=None,
    #                  wwpct:float=None,
    #                  name_mat_basis: str=None,
    #                  err_rel_pct:float=5)->int:

    #     if name_mat is None:
    #         raise ValueError("Flowsheet.put_material(): Material name must be provided.")
    #     if name_mat_basis is None:
    #         raise ValueError("Flowsheet.put_material(): The name of the basis material must be provided.")
    #     # if equiv is None and v_per_w is None:
    #     #     raise ValueError("Flowsheet.put_material(): Either equivalent (equiv) or volume per weight (v_per_w) must be provided.")
    #     # if equiv is not None and v_per_w is not None:
    #     #     raise ValueError("Flowsheet.put_material(): Dual input. Only one of equivalent (equiv) or volume per weight (v_per_w) should be provided.")
    #     count_qty_rel:int = sum(x is not None for x in (equiv, v_per_w, wwpct))
    #     if count_qty_rel == 0:
    #         raise ValueError("Flowsheet.put_material(): One of equivalent (equiv), volume per weight (v_per_w), or weight percent (ww_pct) must be provided.")
    #     elif count_qty_rel > 1:
    #         raise ValueError("Flowsheet.put_material(): Only one of equivalent (equiv), volume per weight (v_per_w), or weight percent (ww_pct) should be provided.")


    #     excel_formular_mat:str=None
    #     if equiv is not None:
    #         excel_formular_mat = f'={alph_col_mat}{self.current_line}&" ("&{alph_col_equiv}{self.current_line}&" equiv vs "&{alph_col_name_basis}{self.current_line}&")"'
    #     elif v_per_w is not None:
    #         excel_formular_mat = f'={alph_col_mat}{self.current_line}&" ("&{alph_col_v_per_w}{self.current_line}&" v/w vs "&{alph_col_name_basis}{self.current_line}&")"'
    #     elif wwpct is not None:
    #         excel_formular_mat = f'={alph_col_mat}{self.current_line}&" ("&{alph_col_wwpct}{self.current_line}&" wt% vs "&{alph_col_name_basis}{self.current_line}&")"'
    #     line_mat = self.put_line(time=time, method=method, content=excel_formular_mat, record=record, operator=operator, witness=witness)

    #     self.ws.cell(row=line_mat, column=col_xlslog_mat).value = name_mat
    #     self.ws.cell(row=line_mat, column=col_xlslog_mw).value = mw if mw is not None else ""
    #     self.ws.cell(row=line_mat, column=col_xlslog_dens).value = dens if dens is not None else ""
    #     self.ws.cell(row=line_mat, column=col_xlslog_assay_conc).value = assay_conc if assay_conc is not None else 100.0
    #     self.ws.cell(row=line_mat, column=col_xlslog_equiv).value = equiv if equiv is not None else ""
    #     self.ws.cell(row=line_mat, column=col_xlslog_v_per_w).value = v_per_w if v_per_w is not None else ""
    #     self.ws.cell(row=line_mat, column=col_xlslog_wwpct).value = wwpct if wwpct is not None else ""
    #     self.ws.cell(row=line_mat, column=col_xlslog_err_rel).value = err_rel_pct

    #     return line_mat

    def put_material(self,
                     time: str ='',
                     method: str='',
                     record: str='',
                     operator: str='',
                     witness: str='',
                     mat_input: Input=None)->int:

        def __put_consts(self,
                         name_mat:str=None,
                         mw:float=None,
                         dens:float=None,
                         assay_conc:float=None,
                         name_basis:float=None,
                         equiv:float=None,
                         v_per_w:float=None,
                         wwpct:float=None,
                         wt_abs_kg_gro:float=None,
                         vol_abs_litre:float=None):
            count_qty_input = sum(x is not None for x in (equiv, v_per_w, wwpct, wt_abs_kg_gro, vol_abs_litre))
            if count_qty_input != 1:
                raise RuntimeError(f'{self.__class__.__name__}.put_material().__put_constants(): Zero or multiple quantifier {count_qty_input}')

            if name_mat is not None:
                self.ws.cell(low=line, column=col_xlslog_mat).value = name_mat
            if mw is not None:
                self.ws.cell(low=line, column=col_xlslog_mw).value = mw
            if dens is not None:
                self.ws.cell(low=line, column=col_xlslog_dens).value = dens
            if assay_conc is not None:
                self.ws.cell(low=line, column=col_xlslog_assay_conc).value = assay_conc
            if name_basis is not None:
                self.ws.cell(low=line, column=col_xlslog_name_basis).value = name_basis
            if equiv is not None:
                self.ws.cell(low=line, column=col_xlslog_equiv).value = equiv
            if v_per_w is not None:
                self.ws.cell(low=line, column=col_xlslog_v_per_w).value = v_per_w
            if wwpct is not None:
                self.ws.cell(low=line, column=col_xlslog_wwpct).value = wwpct
            if wt_abs_kg_gro is not None:
                self.ws.cell(low=line, column=col_xlslog_wt_abs_kg_gro).value = wt_abs_kg_gro
            if vol_abs_litre is not None:
                self.ws.cell(low=line, column=col_xlslog_vol_abs).value = vol_abs_litre

        
        if mat_input is None:
            raise ValueError("Flowsheet.put_material(): Material input (mat_input) must be provided.")

        line = self.current_line
        mat_input.fs_line_mat = line

        excel_formula_mat:str=""
        if mat_input.material_class == chgng.cls_input_mat_sm:
            excel_formula_mat = f'={alph_col_mat}{line}'

        elif mat_input.material_class == chgng.cls_input_mat_tgt:
            excel_formula_mat=''
        else:
            if mat_input.metrics_unit == chgng.opt_mtrcs_eq:
                excel_formula_mat = f'={alph_col_mat}{line}&" ("&{alph_col_equiv}{line}&"equiv vs "&{alph_col_name_basis}{line}&")"'
            elif mat_input.metrics_unit == chgng.opt_mtrcs_v_per_w:
                excel_formula_mat = f'={alph_col_mat}{line}&" ("&{alph_col_v_per_w}{line}&"v/w vs "&{alph_col_name_basis}{line}&")"'
            elif mat_input.metrics_unit == chgng.opt_mtrcs_wwpct:
                excel_formula_mat = f'={alph_col_mat}{line}&" ("&{alph_col_wwpct}{line}&"w/w% vs "&{alph_col_name_basis}{line}&")"'

        self.put_line(time=time,
                      method=method,
                      content=excel_formula_mat,
                      record=record,
                      operator=operator,
                      witness=witness)

#TODO: Please put the constants in the logic field by using __put_consts()


        return line



    def put_qty(self,
                time: str ='',
                method: str='',
                record: str='',
                operator: str='',
                witness: str='',
                line_mat:int=None)->int:
        if line_mat is None:
            raise ValueError("Flowsheet.put_range(): Material line (line_mat) must be provided.")

        excel_formular_qty = f'=TEXT({alph_col_kg_gro}{line_mat},"0.00")&" ± "&TEXT({alph_col_err_abs}{line_mat},"0.00")&" kg"'
        line_qty = self.put_line(time=time, method=method, content=excel_formular_qty, record=record, operator=operator, witness=witness)

        return line_qty

    def put_qty(self, inputs:GetInputs=None, id_input:int=None)->int:
        if inputs is None:
            raise ValueError(f'{self.__class__.__name__}.put_qty(): Material input (inputs:GetInputs) must be provided.')
        if id_input is None:
            raise ValueError(f'{self.__class__.__name__}.put_qty(): id_input must be provided.')

        mat_input = inputs.get_input(id_input=id_input)
        line_fs_this = mat_input.fs_line_mat
        if line_fs_this is None:
            raise RuntimeError(f'{self.__class__.__name__}.put_qty(): '
                               f'Input "{mat_input.material_name}" (ID {mat_input.id_input}) has an empty fs_line_mat.')

        def __prep_ref(alph_col:str=None, list_rows:list[int]=None)->str:
            if alph_col is None:
                raise ValueError(f'{self.__class__.__name__}.put_qty().__prep_ref(): An argument "alph_col" is None. Alphabet column identifier is needed.')
            if list_rows is None or len(list_rows) == 0:
                raise ValueError(f'{self.__class__.__name__}.put_qty().__prep_ref(): An argument "list_rows" is None or len(list_rows)==0. A list of depended row is needed.')
            
            if len(list_rows) == 1:
                return f'={alph_col}{list_rows[0]}'
            else:
                list_cell:list[str] = []
                for row in list_rows:
                    list_cell.append(f'{alph_col}{row}')

                str_all_ref = ','.join(list_cell)
                str_all_ref = '=SUM('+str_all_ref+')'
                return str_all_ref

        def __put_values(name_basis:str=None,
                         list_rows_basis_mol:list[int]=None,
                         list_rows_basis_kg_net:list[int]=None,
                         equiv:float=None,
                         v_per_w:float=None,
                         wwpct:float=None,
                         wt_abs_kg_gro:float=None,
                         vol_abs:float=None):
            count_args_basis = sum(x is not None for x in (list_rows_basis_mol, list_rows_basis_kg_net))
            if count_args_basis == 2:
                raise RuntimeError(f'{self.__class__.__name__}.put_qty().__put_values(): count_args_basis dual input.')            
            count_args_quant =  sum(x is not None for x in (equiv, v_per_w, wwpct, wt_abs_kg_gro, vol_abs))
            if count_args_quant != 1:
                raise RuntimeError(f'{self.__class__.__name__}.put_qty().__put_values(): count_args_quant=={count_args_quant}!= 1.')
            if equiv is not None and not list_rows_basis_mol:
                raise RuntimeError(f'{self.__class__.__name__}.put_qty().__put_values(): An argument "equiv" is provided with empty "list_id_basis_mol".')
            if (v_per_w is not None or wwpct is not None) and not list_rows_basis_kg_net:
                raise RuntimeError(f'{self.__class__.__name__}.put_qty().__put_values(): An argument "v_per_w" or "wwpct" is provided with empty "list_id_basis_kg_net".')
            
            if name_basis is not None:
                self.ws.cell(row=line_fs_this, column=col_xlslog_name_basis).value = name_basis
            else:
                pass

            if list_rows_basis_mol is not None:
                xls_formula_basis = __prep_ref(alph_col=alph_col_mol, list_rows=list_rows_basis_mol)
                self.ws.cell(row=line_fs_this, column=col_xlslog_mol_basis).value = xls_formula_basis
            elif list_rows_basis_kg_net is not None:
                xls_formula_basis = __prep_ref(alph_col=alph_col_kg_net, list_rows=list_rows_basis_kg_net)
                self.ws.cell(row=line_fs_this, column=col_xlslog_kg_net_basis).value = xls_formula_basis
            else:
                pass

            if equiv is not None:
                self.ws.cell(row=line_fs_this, column=col_xlslog_equiv).value = equiv
            elif v_per_w is not None:
                self.ws.cell(row=line_fs_this, column=col_xlslog_v_per_w).value = v_per_w
            elif wwpct is not None:
                self.ws.cell(row=line_fs_this, column=col_xlslog_wwpct).value = wwpct
            elif wt_abs_kg_gro is not None:
                self.ws.cell(row=line_fs_this, column=col_xlslog_wt_abs_kg_gro).value = wt_abs_kg_gro
            elif vol_abs is not None:
                self.ws.cell(row=line_fs_this, column=col_xlslog_vol_abs).value = vol_abs
            else:
                pass

        def __basis_ids_to_lines(list_ids:list[int]=None)->list[int]:
            if not list_ids:
                raise RuntimeError(f'{self.__class__.__name__}.put_qty().__basis_ids_to_lines(): '
                                   '"list_ids" is None or empty.')
            list_lines:list[int]=[]
            for single_id in list_ids:
                basis = inputs.get_input(id_input=single_id)
                list_lines.append(basis.fs_line_mat)
            return list_lines

        if mat_input.metrics_unit == chgng.opt_mtrcs_wt_gro_abs:
            __put_values(name_basis=mat_input.material_name,
                         wt_abs_kg_gro=mat_input.metrics_val)
            return line_fs_this
        elif mat_input.metrics_unit == chgng.opt_mtrcs_vol_abs:
            __put_values(name_basis=mat_input.material_name,
                         vol_abs=mat_input.metrics_val)
            return line_fs_this
        else:
            pass

        list_basis = mat_input.arr_basis_input

        if not list_basis:
            raise RuntimeError(f'{self.__class__.__name__}.put_qty():'
                               f'No basis specified for "{mat_input.material_name}" (input ID: {mat_input.id_input}). '
                               f'Although it metrics_unit is {mat_input.metrics_unit}, which requires at least one basis input.')

        name_basis = (inputs.get_input(id_input=list_basis[0])).material_name
        if mat_input.metrics_unit == chgng.opt_mtrcs_eq:
            __put_values(name_basis=name_basis,
                         list_rows_basis_mol=__basis_ids_to_lines(list_basis),
                         equiv=mat_input.metrics_val)
            return line_fs_this
        elif mat_input.metrics_unit == chgng.opt_mtrcs_v_per_w:
            __put_values(name_basis=name_basis,
                         list_rows_basis_kg_net=__basis_ids_to_lines(list_basis),
                         v_per_w=mat_input.metrics_val)
            return line_fs_this
        elif mat_input.metrics_unit == chgng.opt_mtrcs_wwpct:
            __put_values(name_basis=name_basis,
                         list_rows_basis_kg_net=__basis_ids_to_lines(list_basis),
                         wwpct=mat_input.metrics_val)
            return line_fs_this
        else:
            raise RuntimeError(f'{self.__class__.__name__}: Invalid metrics unit "{mat_input.metrics_unit}" for the input ID {mat_input.id_input} of "{mat_input.material_name}"')

        




    def body_organizer(self,
                       list_col_time: List[str],
                       list_col_method: List[str],
                       list_col_content: List[str],
                       list_col_record: List[str],
                       list_col_operator: List[str],
                       list_col_witness: List[str])->int:
        len_list_time = len(list_col_time)
        for row_rel in range(len_list_time):
            self.ws.cell(row=self.current_line+row_rel, column=col_time).value = list_col_time[row_rel]

        len_list_method = len(list_col_method)
        for row_rel in range(len_list_method):
            self.ws.cell(row=self.current_line+row_rel, column=col_method).value = list_col_method[row_rel]

        len_list_content = len(list_col_content)
        for row_rel in range(len_list_content):
            self.ws.cell(row=self.current_line+row_rel, column=col_content).value = list_col_content[row_rel]

        len_list_record = len(list_col_record)
        for row_rel in range(len_list_record):
            self.ws.cell(row=self.current_line+row_rel, column=col_record).value = list_col_record[row_rel]

        len_list_operator = len(list_col_operator)
        for row_rel in range(len_list_operator):
            self.ws.cell(row=self.current_line+row_rel, column=col_operator).value = list_col_operator[row_rel]

        len_list_witness = len(list_col_witness)
        for row_rel in range(len_list_witness):
            self.ws.cell(row=self.current_line+row_rel, column=col_witness).value = list_col_witness[row_rel]

        list_col_time.clear()
        list_col_method.clear()
        list_col_content.clear()
        list_col_record.clear()
        list_col_operator.clear()
        list_col_witness.clear()

        max_length = max(len_list_time,
                         len_list_method,
                         len_list_content,
                         len_list_record,
                         len_list_operator,
                         len_list_witness)
        
        for row_rel in range(max_length):
            self.ws.cell(row=self.current_line + row_rel, column=col_method).border = border_left
            self.__put_excel_logic(line=self.current_line + row_rel)

        self.current_line += max_length
        return self.current_line-1



    def __put_excel_logic(self, line:int=None)->None:
        #Background
        if line == line_xlslog_hedr:
            #Standard
            # self.ws.cell(row=line, column=col_xlslog_mol-1).value = dict_part_logic[tag_part_std_mol] 
            # self.ws.cell(row=line, column=col_xlslog_mol).value = self.mol_std
            # self.ws.cell(row=line, column=col_xlslog_mol).fill = fill_light_orange
            # # self.ws.cell(row=line, column=col_xlslog_mol).border = border_around

            # self.ws.cell(row=line, column=col_xlslog_kg_net-1).value = dict_part_logic[tag_part_std_wt_net]
            # self.ws.cell(row=line, column=col_xlslog_kg_net).value = self.wt_net_std
            # self.ws.cell(row=line, column=col_xlslog_kg_net).fill = fill_light_orange
            # self.ws.cell(row=line, column=col_xlslog_kg_net).border = border_around
            
            #Header
            self.ws.cell(row=line, column=col_xlslog_mat).value = dict_part_logic[tag_part_hedr_mat]
            self.ws.cell(row=line, column=col_xlslog_mat).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_mat).border = border_around
            self.ws.cell(row=line, column=col_xlslog_mat).font = font_bold
            
            self.ws.cell(row=line, column=col_xlslog_mw).value = dict_part_logic[tag_part_hedr_mw]
            self.ws.cell(row=line, column=col_xlslog_mw).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_mw).border = border_around
            self.ws.cell(row=line, column=col_xlslog_mw).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_dens).value = dict_part_logic[tag_part_hedr_dens]
            self.ws.cell(row=line, column=col_xlslog_dens).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_dens).border = border_around
            self.ws.cell(row=line, column=col_xlslog_dens).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_assay_conc).value = dict_part_logic[tag_part_hedr_assay_conc]
            self.ws.cell(row=line, column=col_xlslog_assay_conc).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_assay_conc).border = border_around
            self.ws.cell(row=line, column=col_xlslog_assay_conc).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_name_basis).value = dict_part_logic[tag_part_hedr_name_basis]
            self.ws.cell(row=line, column=col_xlslog_name_basis).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_name_basis).border = border_around
            self.ws.cell(row=line, column=col_xlslog_name_basis).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_mol_basis).value = dict_part_logic[tag_part_hedr_mol_basis]
            self.ws.cell(row=line, column=col_xlslog_mol_basis).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_mol_basis).border = border_around
            self.ws.cell(row=line, column=col_xlslog_mol_basis).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_kg_net_basis).value = dict_part_logic[tag_part_hedr_kg_net_basis]
            self.ws.cell(row=line, column=col_xlslog_kg_net_basis).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_kg_net_basis).border = border_around
            self.ws.cell(row=line, column=col_xlslog_kg_net_basis).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_equiv).value = dict_part_logic[tag_part_hedr_equiv]
            self.ws.cell(row=line, column=col_xlslog_equiv).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_equiv).border = border_around
            self.ws.cell(row=line, column=col_xlslog_equiv).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_v_per_w).value = dict_part_logic[tag_part_hedr_v_per_w]
            self.ws.cell(row=line, column=col_xlslog_v_per_w).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_v_per_w).border = border_around
            self.ws.cell(row=line, column=col_xlslog_v_per_w).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_wwpct).value = dict_part_logic[tag_part_hedr_wwpct]
            self.ws.cell(row=line, column=col_xlslog_wwpct).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_wwpct).border = border_around
            self.ws.cell(row=line, column=col_xlslog_wwpct).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_wt_abs_kg_gro).value = dict_part_logic[tag_part_hedr_wt_gro_abs]
            self.ws.cell(row=line, column=col_xlslog_wt_abs_kg_gro).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_wt_abs_kg_gro).border = border_around
            self.ws.cell(row=line, column=col_xlslog_wt_abs_kg_gro).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_vol_abs).value = dict_part_logic[tag_part_hedr_vol_abs]
            self.ws.cell(row=line, column=col_xlslog_vol_abs).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_vol_abs).border = border_around
            self.ws.cell(row=line, column=col_xlslog_vol_abs).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_mol).value = dict_part_logic[tag_part_hedr_mol]
            self.ws.cell(row=line, column=col_xlslog_mol).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_mol).border = border_around
            self.ws.cell(row=line, column=col_xlslog_mol).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_volume).value = dict_part_logic[tag_part_hedr_volume]
            self.ws.cell(row=line, column=col_xlslog_volume).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_volume).border = border_around
            self.ws.cell(row=line, column=col_xlslog_volume).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_kg_net).value = dict_part_logic[tag_part_hedr_kg_net]
            self.ws.cell(row=line, column=col_xlslog_kg_net).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_kg_net).border = border_around
            self.ws.cell(row=line, column=col_xlslog_kg_net).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_kg_gro).value = dict_part_logic[tag_part_hedr_kg_gro]
            self.ws.cell(row=line, column=col_xlslog_kg_gro).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_kg_gro).border = border_around
            self.ws.cell(row=line, column=col_xlslog_kg_gro).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_err_rel).value = dict_part_logic[tag_part_hedr_err_rel]
            self.ws.cell(row=line, column=col_xlslog_err_rel).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_err_rel).border = border_around
            self.ws.cell(row=line, column=col_xlslog_err_rel).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_err_abs).value = dict_part_logic[tag_part_hedr_err_abs]
            self.ws.cell(row=line, column=col_xlslog_err_abs).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_err_abs).border = border_around
            self.ws.cell(row=line, column=col_xlslog_err_abs).font = font_bold
            
        # elif line == line_standard + 1:
        #     pass
        else:
            cell_equiv = f'{alph_col_equiv}{line}'
            cell_v_per_w = f'{alph_col_v_per_w}{line}'
            cell_wwpct = f'{alph_col_wwpct}{line}'
            cell_wt_abs_gro = f'{alph_col_kg_gro_abs}{line}'
            cell_vol_abs = f'{alph_col_vol_abs}{line}'

            cell_mol_basis = f'{alph_col_mol_basis}{line}'
            cell_kg_net_basis = f'{alph_col_kg_net_basis}{line}'
            
            cell_mw = f'{alph_col_mw}{line}'
            cell_dens = f'{alph_col_dens}{line}'
            cell_assay_conc = f'{alph_col_assay_conc}{line}'

            cell_kg_gro=f'{alph_col_kg_gro}{line}'
            cell_kg_net=f'{alph_col_kg_net}{line}'

            cell_err_rel = f'{alph_col_err_rel}{line}'

            #mol
            xls_formular_mol = (f'=_xlfn.IFS({cell_equiv}<>"",{cell_mol_basis}*{cell_equiv},'
                                f'AND({cell_v_per_w}<>"", {cell_mw}<>"", {cell_assay_conc}<>"", {cell_dens}<>""),{cell_kg_net_basis}*{cell_v_per_w}*{cell_dens}*({cell_assay_conc}/100)*1000/{cell_mw},'
                                #f'AND({cell_v_per_w}<>"", {cell_mw}<>"", {cell_assay_conc}<>"", {cell_dens}<>""),{cell_kg_net}*1000/{cell_mw},'
                                f'AND({cell_wwpct}<>"", {cell_mw}<>""), {cell_kg_net_basis}*({cell_wwpct}/100)*1000/{cell_mw},'
                                f'AND({cell_wt_abs_gro}<>"", {cell_assay_conc}<>"", {cell_mw}<>""), {cell_wt_abs_gro}*({cell_assay_conc}/100)*1000/{cell_mw},'
                                f'AND({cell_vol_abs}<>"", {cell_dens}<>"", {cell_assay_conc}<>"", {cell_mw}<>""), {cell_vol_abs}*{cell_dens}*({cell_assay_conc}/100)*1000/{cell_mw},'
                                #f'AND({cell_equiv}="",{cell_v_per_w}="",{cell_wwpct}="",{cell_assay_conc}<>"",{cell_mw}<>""),{cell_kg_gro}*({cell_assay_conc}/100)*1000/{cell_mw},'
                                 'TRUE,"")')
            self.ws.cell(row=line, column=col_xlslog_mol).value = xls_formular_mol
            #v/w
            xls_formular_volume = (f'=_xlfn.IFS(AND({cell_equiv}<>"", {cell_mw}<>"", {cell_dens}<>""), {cell_mol_basis}*{cell_equiv}*{cell_mw}/1000/{cell_dens},'
                                #    f'AND(OR({cell_equiv}<>"", {cell_wwpct}<>""),{cell_dens}>0, {cell_dens}<>""),{alph_col_kg_gro}{line}/{cell_dens},'
                                   f'{cell_v_per_w}<>"",{cell_kg_net_basis}*{cell_v_per_w},'
                                   f'AND({cell_wwpct}<>"",{cell_dens}<>""), {cell_kg_net_basis}*({cell_wwpct}/100)/{cell_dens},'
                                   f'AND({cell_wt_abs_gro}<>"", {cell_dens}<>""), {cell_wt_abs_gro}/{cell_dens},'
                                   f'{cell_vol_abs}<>"",{cell_vol_abs},'
                                 'TRUE,"")')
            self.ws.cell(row=line, column=col_xlslog_volume).value = xls_formular_volume

            # #w/w%
            # xls_formular_wwpct = f'=IF({alph_col_wwpct}{line}<>"",{alph_col_kg_net_basis}{line}*{alph_col_wwpct}{line}/100,"")'
            # self.ws.cell(row=line, column=col_xlslog_wwpct).value = xls_formular_wwpct

            #kg_net
            xls_formular_kg_net = (f'=_xlfn.IFS(AND({cell_equiv}<>"",{cell_mw}<>""),{cell_mol_basis}*{cell_equiv}*{cell_mw}/1000,'
                                           f'AND({cell_v_per_w}<>"",{cell_assay_conc}<>"", {cell_dens}<>""), {cell_kg_net_basis}*{cell_v_per_w}*{cell_dens}*({cell_assay_conc}/100),'
                                           f'AND({cell_wwpct}<>"", {cell_assay_conc}<>""), {cell_kg_net_basis}*({cell_wwpct}/100),'
                                           f'AND({cell_wt_abs_gro}<>"", {cell_assay_conc}<>""),{cell_wt_abs_gro}*({cell_assay_conc}/100),'
                                           f'AND({cell_vol_abs}<>"", {cell_dens}<>"", {cell_assay_conc}<>""), {cell_vol_abs}*{cell_dens}*({cell_assay_conc}/100),'
                                           'TRUE,"")')
            self.ws.cell(row=line, column=col_xlslog_kg_net).value = xls_formular_kg_net
            #kg_gro
            #xls_formular_kg_gro = (f'=IF({alph_col_kg_net}{line}<>"",{alph_col_kg_net}{line}/({alph_col_assay_conc}{line}/100),"")')
            xls_formular_kg_gro = (f'=_xlfn.IFS(AND({cell_equiv}<>"", {cell_mw}<>"", {cell_assay_conc}<>""), {cell_mol_basis}*{cell_equiv}*{cell_mw}/({cell_assay_conc}/100)/1000,'
                                   f'AND({cell_v_per_w}<>"",{cell_dens}<>""), {cell_kg_net_basis}*{cell_v_per_w}*{cell_dens},'
                                   f'AND({cell_wt_abs_gro}<>""),{cell_wt_abs_gro},'
                                   f'AND({cell_vol_abs}<>"", {cell_dens}<>""), {cell_vol_abs}*{cell_dens},'
                                   'TRUE,"")')
            self.ws.cell(row=line, column=col_xlslog_kg_gro).value = xls_formular_kg_gro
            #err_abs
            xls_formular_err_abs = f'=IF(AND({cell_kg_gro}<>"",{cell_err_rel}<>""),{cell_kg_gro}*{cell_err_rel}/100,"")'
            self.ws.cell(row=line, column=col_xlslog_err_abs).value = xls_formular_err_abs

            #Formatting
            self.ws.cell(row=line, column=col_xlslog_mat).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_mat).border = border_around
            
            self.ws.cell(row=line, column=col_xlslog_mw).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_mw).border = border_around

            self.ws.cell(row=line, column=col_xlslog_dens).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_dens).border = border_around

            self.ws.cell(row=line, column=col_xlslog_assay_conc).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_assay_conc).border = border_around

            self.ws.cell(row=line, column=col_xlslog_equiv).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_equiv).border = border_around

            self.ws.cell(row=line, column=col_xlslog_v_per_w).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_v_per_w).border = border_around

            self.ws.cell(row=line, column=col_xlslog_wwpct).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_wwpct).border = border_around

            self.ws.cell(row=line, column=col_xlslog_wt_abs_kg_gro).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_wt_abs_kg_gro).border = border_around

            self.ws.cell(row=line, column=col_xlslog_vol_abs).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_vol_abs).border = border_around

            self.ws.cell(row=line, column=col_xlslog_mol).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_mol).border = border_around

            self.ws.cell(row=line, column=col_xlslog_volume).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_volume).border = border_around

            self.ws.cell(row=line, column=col_xlslog_kg_net).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_kg_net).border = border_around

            self.ws.cell(row=line, column=col_xlslog_kg_gro).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_kg_gro).border = border_around

            self.ws.cell(row=line, column=col_xlslog_err_rel).fill = fill_light_orange
            self.ws.cell(row=line, column=col_xlslog_err_rel).border = border_around

            self.ws.cell(row=line, column=col_xlslog_err_abs).fill = fill_light_blue
            self.ws.cell(row=line, column=col_xlslog_err_abs).border = border_around


    
    def linefeed(self)->int:
        self.ws.cell(row=self.current_line, column=col_method).border = border_left
        self.__put_excel_logic(self.current_line)
        self.current_line += 1
        return self.current_line-1

    def save(self, filename: str):
        self.wb.save(filename=filename)











    