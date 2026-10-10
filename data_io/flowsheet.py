import openpyxl as xl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment, PatternFill, Font
from typing import List
import re
import flow_draw.definitions as defs
import math



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
col_xlslog_equiv = 14
col_xlslog_v_per_w = 15
col_xlslog_mol = 16
col_xlslog_volume = 17
col_xlslog_kg_net = 18
col_xlslog_kg_gro = 19
col_xlslog_err_rel = 20
col_xlslog_err_abs = 21

col_xlslog_name_basis = 23
col_xlslog_id_basis = 24
col_xlslog_class = 25
col_xlslog_mol_std = 26
col_xlslog_kg_net_std = 27





tag_part_hedr_mat = "tag_hedr_mat"
"""Tag for header material"""
tag_part_hedr_mw = "tag_hedr_mw"
"""Tag for header molecular weight"""
tag_part_hedr_dens = "tag_hedr_dens"
"""Tag for header density"""
tag_part_hedr_assay_conc = "tag_hedr_assay_conc"
"""Tag for header assay concentration"""
tag_part_hedr_equiv = "tag_hedr_equiv"
"""Tag for header equivalent"""
tag_part_hedr_v_per_w = "tag_hedr_v/w"
"""Tag for header volume per weight"""
tag_part_hedr_mol = "tag_hedr_mol"
"""Tag for header mol"""
tag_part_hedr_volume = "tag_hedr_volume"
"""Tag for header volume"""
tag_part_hedr_kg_net = "tag_hedr_kg_net"
"""Tag for header net weight"""
tag_part_hedr_kg_gro = "tag_hedr_kg_gro"
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
                     tag_part_hedr_equiv: "Equiv",
                     tag_part_hedr_v_per_w: "v/w",
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
alph_col_equiv = num_to_alph(num_col = col_xlslog_equiv)
alph_col_v_per_w = num_to_alph(num_col = col_xlslog_v_per_w)
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
        self.dict_basis:dict{int, int} = {}

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

    def put_material(self,
                     time: str ='',
                     method: str='',
                     record: str='',
                     operator: str='',
                     witness: str='',
                     name_mat:str=None,
                     mw:float=None,
                     dens:float=None,
                     assay_conc:float=None,
                     equiv:float=None,
                     v_per_w:float=None,
                     name_mat_basis: str=None,
                     err_rel_pct:float=5)->int:

        if name_mat is None:
            raise ValueError("Flowsheet.put_material(): Material name must be provided.")
        if name_mat_basis is None:
            raise ValueError("Flowsheet.put_material(): The name of the basis material must be provided.")
        if equiv is None and v_per_w is None:
            raise ValueError("Flowsheet.put_material(): Either equivalent (equiv) or volume per weight (v_per_w) must be provided.")
        if equiv is not None and v_per_w is not None:
            raise ValueError("Flowsheet.put_material(): Dual input. Only one of equivalent (equiv) or volume per weight (v_per_w) should be provided.")
        
        excel_formular_mat:str=None
        if equiv is not None:
            excel_formular_mat = f'={alph_col_mat}{self.current_line}&" ("&{alph_col_equiv}{self.current_line}&" equiv.)"'
        elif v_per_w is not None:
            excel_formular_mat = f'={alph_col_mat}{self.current_line}&" ("&{alph_col_v_per_w}{self.current_line}&" v/w)"'
        line_mat = self.put_line(time=time, method=method, content=excel_formular_mat, record=record, operator=operator, witness=witness)

        self.ws.cell(row=line_mat, column=col_xlslog_mat).value = name_mat
        self.ws.cell(row=line_mat, column=col_xlslog_mw).value = mw if mw is not None else ""
        self.ws.cell(row=line_mat, column=col_xlslog_dens).value = dens if dens is not None else ""
        self.ws.cell(row=line_mat, column=col_xlslog_assay_conc).value = assay_conc if assay_conc is not None else 100
        self.ws.cell(row=line_mat, column=col_xlslog_equiv).value = equiv if equiv is not None else ""
        self.ws.cell(row=line_mat, column=col_xlslog_v_per_w).value = v_per_w if v_per_w is not None else ""
        self.ws.cell(row=line_mat, column=col_xlslog_err_rel).value = err_rel_pct

        return line_mat

    def put_qty(self,
                time: str ='',
                method: str='',
                record: str='',
                operator: str='',
                witness: str='',
                line_mat:int=None)->int:
        if line_mat is None:
            raise ValueError("Flowsheet.put_qty(): Material line (line_mat) must be provided.")

        excel_formular_qty = f'=TEXT({alph_col_kg_gro}{line_mat},"0.00")&" ± "&TEXT({alph_col_err_abs}{line_mat},"0.00")&" kg"'
        line_qty = self.put_line(time=time, method=method, content=excel_formular_qty, record=record, operator=operator, witness=witness)

        return line_qty


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

            self.ws.cell(row=line, column=col_xlslog_equiv).value = dict_part_logic[tag_part_hedr_equiv]
            self.ws.cell(row=line, column=col_xlslog_equiv).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_equiv).border = border_around
            self.ws.cell(row=line, column=col_xlslog_equiv).font = font_bold

            self.ws.cell(row=line, column=col_xlslog_v_per_w).value = dict_part_logic[tag_part_hedr_v_per_w]
            self.ws.cell(row=line, column=col_xlslog_v_per_w).fill = fill_lighter_orange
            self.ws.cell(row=line, column=col_xlslog_v_per_w).border = border_around
            self.ws.cell(row=line, column=col_xlslog_v_per_w).font = font_bold

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
            #mol
            xls_formular_mol = f'=IF({alph_col_equiv}{line}<>"",${alph_col_mol}${line_standard}*{alph_col_equiv}{line},"")'
            self.ws.cell(row=line, column=col_xlslog_mol).value = xls_formular_mol
            #volume
            xls_formular_volume = f'=IF({alph_col_v_per_w}{line}<>"",${alph_col_kg_net}${line_standard}*{alph_col_v_per_w}{line},"")'
            self.ws.cell(row=line, column=col_xlslog_volume).value = xls_formular_volume
            #kg_net
            xls_formular_kg_net = (f'=_xlfn.IFS({alph_col_mol}{line}<>"",{alph_col_mol}{line}*{alph_col_mw}{line}/1000,'
                               f'{alph_col_volume}{line}<>"",{alph_col_volume}{line}*{alph_col_dens}{line},'
                               'TRUE,"")')
            self.ws.cell(row=line, column=col_xlslog_kg_net).value = xls_formular_kg_net
            #kg_gro
            xls_formular_kg_gro = f'=IF({alph_col_kg_net}{line}<>"",{alph_col_kg_net}{line}/({alph_col_assay_conc}{line}/100),"")'
            self.ws.cell(row=line, column=col_xlslog_kg_gro).value = xls_formular_kg_gro
            #err_abs
            xls_formular_err_abs = f'=IF({alph_col_kg_gro}{line}<>"",{alph_col_kg_gro}{line}*{alph_col_err_rel}{line}/100,"")'
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











    