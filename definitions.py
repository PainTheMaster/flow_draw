import openpyxl as xl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment
from openpyxl.styles import Font

############################
#        Parameters        #
############################
#Batch IO
dflt_io_batch_num_procs = 100

#MATERIALS
dflt_mats_num_rows = 100



###############################################
#ITEMS FOR INTERNAL DATA PROCESSING: TAGS ETC #
###############################################

#general
opt_yes: str = 'Yes'
"""An affirmative option"""
opt_no: str = 'No'
"""An negative option"""
list_yesno: list[str]=[opt_no, opt_yes]
"""List of affirmative and negative options"""

#Unit
opt_second:str = "s"
"""Option for a time unit: second"""
opt_minute:str = "min"
"""Option for a time unit: minute"""
opt_hour:str = "hr"
"""Option for a time unit: hour"""
list_time_unit:list[str] = [opt_second, opt_minute, opt_hour]
"""List of time units"""

#unit_operations
tag_uo_line_clearance: str = "line_clearance"
"""Tag for an unit operation line clearance"""
part_uo_title_clearance_jp = "ラインクリアランス"
"""JP expression of line clearance"""

tag_uo_innert_replace: str = "innert_gas_placement"
"""Tag for an unit operation N2 replacement"""
part_uo_title_innert_replace_jp = "減圧不活性ガス置換"
"""JP expression of N2 replacement"""

tag_uo_tempr_ctrl: str = "temp_control"
"""Tag for an unit operation for temperature control"""
part_uo_title_tempr_ctrl_jp = "温調"
"""JP expression of temperature control"""

tag_uo_charging: str = "charging"
"""Tag for an unit operation charging/dosing"""
part_uo_title_charging_jp = "仕込み"
"""JP expression of charging/dosing"""

tag_uo_agitation: str = "agitation"
"""Tag for an unit operation agitation/mixing"""
part_uo_title_agitation_jp = "攪拌"
"""JP expression of agitation"""

tag_uo_settling: str = "settling"
"""Tag for an unit operation settling"""
part_uo_title_settling_jp = "静置"
"""JP expression of settling"""

tag_uo_phase_disch: str = "phase_discharge"
"""Tag for an unit operation discharging the lower phase"""
part_uo_title_phase_disch_jp = "下層排出"
"""JP expression of discharging the lower phase"""

tag_uo_evap: str = "evaporation"
"""Tag for an unit operation dietillation"""
part_uo_title_evap_jp = "濃縮" 
"""JP expression of """

tag_uo_cip: str = "cip"
"""Tag for in-process cleaning in place"""
part_uo_title_cip_jp = "工程内洗浄"
"""JP expression of in-process cleaning in place"""

tag_uo_transfer: str = "transfer"
"""Tag for an unit operation liquid transfer"""
part_uo_title_transfer_jp = "移送"
"""JP expression of liquid transfer"""

tag_uo_filt: str = "filtration"
"""Tag for an unit operation filtration of (normally) recrystallizaion slurry"""
part_uo_title_filt_jp = "ろ過"
"""JP expression of filtration"""

tag_uo_cake_rinse: str = "rinse"
"""Tag for an unit operation rinsing filter cake"""
part_uo_title_cake_rinse_jp = "湿性末リンス"
"""JP expression of rinsing filter cake rinsing"""

tag_uo_reslurry: str = "reslurry"
"""Tag for an unit operation reslurry washing of obtained crystals (wet cake)"""
part_uo_title_reslurry_jp = "結晶洗浄"
"""JP expression of reslurry wash of the obtained crystals (wet cake)"""

tag_uo_drying: str = "drying"
"""Tag for an unit operation drying wet filter cake"""
part_uo_title_drying_jp = "乾燥"
"""JP expression of product drying"""

tag_uo_tare_pkg: str = "tare"
"""Tag for an unit operation taring packaging material before discharge"""
part_uo_title_tare_pkg_jp = "風袋秤量"
"""JP expression of taring packaging material before ischarge"""

tag_uo_prod_disch: str = "prod_discharge"
"""Tag for an unit operation discharging finished product"""
part_uo_title_prod_disch_jp = "取出し"
"""JP expression of product discharge"""

tag_uo_prod_weigh: str = "prod_weighing"
"""Tag for an unit operation discharging finished product"""
part_uo_title_prod_weigh_jp = "秤量"
"""JP expression of product discharge"""

tag_uo_placeholder: str = "placeholder"
"""Tag for a placeholder for an undefined unit operation..."""
part_uo_title_placeholder = "<Op. place holder>"
"""JP expression of place holder"""

dict_jp_part_uo_titles = {tag_uo_line_clearance : part_uo_title_clearance_jp,
                          tag_uo_innert_replace : part_uo_title_innert_replace_jp,
                          tag_uo_tempr_ctrl : part_uo_title_tempr_ctrl_jp,
                          tag_uo_charging : part_uo_title_charging_jp,
                          tag_uo_agitation : part_uo_title_agitation_jp,
                          tag_uo_settling : part_uo_title_settling_jp,
                          tag_uo_phase_disch : part_uo_title_phase_disch_jp,
                          tag_uo_evap : part_uo_title_evap_jp,
                          tag_uo_cip : part_uo_title_cip_jp,
                          tag_uo_transfer : part_uo_title_transfer_jp,
                          tag_uo_filt : part_uo_title_filt_jp,
                          tag_uo_cake_rinse : part_uo_title_cake_rinse_jp,
                          tag_uo_reslurry : part_uo_title_reslurry_jp,
                          tag_uo_drying : part_uo_title_drying_jp,
                          tag_uo_tare_pkg : part_uo_title_tare_pkg_jp,
                          tag_uo_prod_disch : part_uo_title_prod_disch_jp,
                          tag_uo_prod_weigh : part_uo_title_prod_weigh_jp,
                          tag_uo_placeholder : part_uo_title_placeholder}
"""dict[<tag>:<unit operation name] for unit operation name in local language}"""

################################################################
#               PARTS FOR BATCH  OUTLINE WORKSHEET             #
################################################################

#>>>>>>>>>>>>>>>>>> file and sheet name <<<<<<<<<<<<<<<<<<<<#
src_io_batch_input_file_name:str = "batch_outline.xlsx"
src_io_batch_outline_ws:str = "batch outline"
"""Worksheet name for the batch outline"""


#>>>>>>>>>>>>>>>>>> header items for batch and some process summary <<<<<<<<<<<<<<<<<<#
hedr_io_batch_item:str ='Item'
"""Header for the item column in the batch outline table"""
hedr_io_batch_value:str='Value'
"""Header for the value column in the batch outline table"""
item_io_batch_batch_name:str = 'Batch Name'
"""Item for the batch name"""
item_io_batch_batch_remark:str = 'Remark for batch'
"""Item for the batch comment"""
item_io_batch_proc_name_stem:str = 'Name, Process-{}'
"""Item for the name of each process. The numbers 1, 2, 3... follow for each step."""
item_io_batch_proc_count_uo_stem:str = 'Count Subitems, Process-{}'
"""Item stem for the count of each process sub-items. The numbers 1, 2, 3 follow for each step"""
item_io_batch_proc_remark_stem:str = 'Remark, Process-{}' 
"""Ietm stem for the comment of each process. The numbers 1, 2, 3 follow for each step"""


#>>>>>>>>>>>>>>>>>> table schema of the process outline worksheet<<<<<<<<<<<<<<<<<<#
row_io_batch_hedr_ouln_tab:int = 0
"""Column number for the items in the table"""
col_io_batch_item_ouln_tab:int = 0
"""Column number for the items in the table"""
col_io_batch_value_ouln_tab:int = 1
"""Column number for the items in the table"""

################################################################################################################################
#                              PARTS FOR PROCESS DATA IO: HEADER ITEMS, DROP-DOWN OPTIONS ETC                                  #
################################################################################################################################


        #>>>>>>>>>>>>>> file name, sheet name <<<<<<<<<<<<<<<<<<#

src_io_filebasename = "_process_input"
"""Base name for process input Excel file"""
src_io_sfx_sumry_ws = "_summary"
"""suffix for summary input worksheet (tab)"""
src_io_sfx_mats_ws:str = "_materials"
"""Suffix for raw material information input worksheet"""
src_io_sfx_detail_ws = "_detail"
"""suffix for detail input worksheet (tab)"""



        #>>>>>>>>>>> header items for summary worksheet <<<<<<<<<<<<<<#

hedr_io_sumry_seq = 'Seq Nr'
"""Header item for sequence number in the process summary worksheet"""
hedr_io_summary_uo = 'Unit Operation'
"""Header item for unit operations in the process summary worksheet"""
hedr_io_sumry_num_subitms = 'Number of Subitems'
"""Header item for number of subitems for each unit operation in the process summary worksheet"""
hedr_io_sumry_edt_cmnt = 'Edit Comment'
"""Header item for edit comment in the process summary worksheet"""

col_nr_io_sumry_seq = 1
"""Column number designator of sequence numbers in the summary worksheet"""
col_nr_io_sumry_uo = 2
"""Column number designator of unit operations in the summary worksheet"""
col_nr_io_sumry_num_subitms = 3
"""Column number designator of number of subitems for each unit operation in the summary worksheet"""
col_nr_io_sumry_edt_cmnt = 4
"""Column number designator of edit comment in the summary worksheet"""



        #>>>>>>>>>>>> header items for material worksheets <<<<<<<<<<<<#

hedr_io_mats_mat:str = "Material"
"""header item for the column for raw material names"""
hedr_io_mats_main = "Main(*)"
"""Header item for the column to identify the core raw materials"""
hedr_io_mats_mw:str = "MW (g/mol)"
"""Header item for the column for molecular weight"""
hedr_io_mats_dnsty:str = "Density (g/mL)"
"""The header for the density/specific gravity of the raw material"""
hedr_io_mats_concasy:str = "Conc/Assay(%)"
"""The header for the concentration or assay of the raw material"""
hedr_io_mats_kgmain:str = "Weight Main (kg)"
"""Header item for the weight of core building block weight (kg)"""
hedr_io_mats_remark:str = "Remark"
"""The header for optional remarks"""

col_nr_io_mats_mat:int = 1
"""Column number for material names"""
col_nr_io_mats_main:int = 2
"""Column number for the main material star (*)"""
col_nr_io_mats_mw : int= 3
"""Column number for molecular weights"""
col_nr_io_mats_dnsty: int = 4
"""Comlumn number for density"""
col_nr_io_mats_concasy: int = 5
"""Column number for concentration or assay"""
col_nr_io_mats_kgmain:int = 6
"""Column number for weight of the core building block"""
col_nr_io_mats_remark: int = 7
"""Column number for comment"""

list_hedr_mats_io: list[str] = [hedr_io_mats_mat,
                               hedr_io_mats_main,
                               hedr_io_mats_mw,
                               hedr_io_mats_dnsty,
                               hedr_io_mats_concasy,
                               hedr_io_mats_kgmain,
                               hedr_io_mats_remark]

itm_io_mats_desig_star:str = "*"
"""Star (*) marker to indicate the core raw material"""



            ##### header items for detail worksheet######

hedr_cmn_io_dtil_seq = hedr_io_sumry_seq
"""Header item for <> in the process detail worksheet"""
hedr_cmn_io_dtil_uo = hedr_io_summary_uo
"""Header item for <> in the process detail worksheet"""
hedr_cmn_io_dtil_edt_cmnt = hedr_io_sumry_edt_cmnt
"""Header item for <> in the process detail worksheet"""
hedr_cmn_io_dtil_precmnt = 'Pre-comment'
"""Header item for <> in the process detail worksheet"""
hedr_cmn_io_dtil_postcmnt = 'Post-comment'
"""Header item for <> in the process detail worksheet"""

list_hedr_cmn_io_dtil = [
    hedr_cmn_io_dtil_seq,
    hedr_cmn_io_dtil_uo,
    hedr_cmn_io_dtil_edt_cmnt,
    hedr_cmn_io_dtil_precmnt,
    hedr_cmn_io_dtil_postcmnt 
]

itm_cmn_io_nocmnt_instr = '(No comment here)'



######################################################
####       CHARGING HEADER ITEMS AND OPTIONS      ####
######################################################
hedr_uo_chgng_mat = 'Material Name'
hedr_uo_chgng_mtrcs_val = 'Metrics Value'
hedr_uo_chgng_mtrcs_unit = 'Metrics Unit'
hedr_uo_chgng_errperm = 'Permissible Error (%)'
hedr_uo_chgng_method = 'Charging Method'
hedr_uo_chgng_timctrl = 'Time Control'
hedr_uo_chgng_timmin = 'Minimum Time (min)'
hedr_uo_chgng_timmax = 'Maximum Time (min)'
hedr_uo_chgng_tempctrl = 'Temp Control'
hedr_uo_chgng_tempmin = 'Minimum Temp (deg-C)'
hedr_uo_chgng_tempmax = 'Maximum Temp (deg-C)'

list_hedr_uo_chgng = [hedr_uo_chgng_mat,
                      hedr_uo_chgng_mtrcs_val,
                      hedr_uo_chgng_mtrcs_unit,
                      hedr_uo_chgng_errperm,
                      hedr_uo_chgng_method,
                      hedr_uo_chgng_timctrl,
                      hedr_uo_chgng_timmin,
                      hedr_uo_chgng_timmax,
                      hedr_uo_chgng_tempctrl,
                      hedr_uo_chgng_tempmin,
                      hedr_uo_chgng_tempmax]

####CHARGING OPTIONS####
opt_uo_chgng_mtrcs_eq = "equiv"
opt_uo_chgng_mtrcs_vol = "v/w"
list_opt_uo_chgng_mtrcs = [opt_uo_chgng_mtrcs_eq, opt_uo_chgng_mtrcs_vol]
"""For process.unit_operations.charging.Charging. This is for drop-down list in the detail input form."""

opt_uo_chgng_method_liq = 'liquid_port'
opt_uo_chgng_method_shower = 'shower'
opt_uo_chgng_method_prssvesl = 'press_vessel'
opt_uo_chgng_method_pwdr ='powder_port'
opt_uo_chgng_method_method_plchldr = 'placeholder'
list_opt_uo_chgng_method =[opt_uo_chgng_method_liq,
                           opt_uo_chgng_method_shower,
                           opt_uo_chgng_method_prssvesl,
                           opt_uo_chgng_method_pwdr,
                           opt_uo_chgng_method_method_plchldr]


opt_uo_chgng_timctrl_none = "No time control"
opt_uo_chgng_timctrl_min="Time control with minimum"
opt_uo_chgng_timctrl_max="Time control with maximum"
opt_uo_chgng_timctrl_min_max='Time control with minimum and maximum'
opt_uo_chgng_timctrl_plchldr = 'Placeholder'
list_opt_uo_chgng_timctrl=[opt_uo_chgng_timctrl_none,
                           opt_uo_chgng_timctrl_min,
                           opt_uo_chgng_timctrl_max,
                           opt_uo_chgng_timctrl_min_max,
                           opt_uo_chgng_timctrl_plchldr]


opt_uo_chgng_temprctrl_none = "No temp control"
opt_uo_chgng_temprctrl_min="Temp control with minimum"
opt_uo_chgng_temprctrl_max="Temp control with maximum"
opt_uo_chgng_temprctrl_min_max='Temp control with minimum and maximum'
opt_uo_chgng_temprctrl_plchldr = 'Placeholder'
list_opt_uo_chgne_temprctrl = [opt_uo_chgng_temprctrl_none,
                               opt_uo_chgng_temprctrl_min,
                               opt_uo_chgng_temprctrl_max,
                               opt_uo_chgng_temprctrl_min_max,
                               opt_uo_chgng_temprctrl_plchldr]


opt_uo_chgng_err_rng_plchldr='place holder'


dict_opt_uo_chgng = {hedr_uo_chgng_mtrcs_unit : list_opt_uo_chgng_mtrcs,
                     hedr_uo_chgng_method : list_opt_uo_chgng_method,
                     hedr_uo_chgng_timctrl : list_opt_uo_chgng_timctrl,
                     hedr_uo_chgng_tempctrl : list_opt_uo_chgne_temprctrl}


######################################################
####     PLACEHOLDER HEADER ITEMS AND OPTIONS     ####
######################################################
hedr_uo_plchldr_lines = "Lines"
"""Header item for the number of lines in unit operation 'place holder' """

list_hedr_uo_plchldr = [hedr_uo_plchldr_lines]



######################################################
##      LINE_CLEARNCE HEADER ITEMS AND OPTIONS      ##
######################################################
hedr_uo_lnclrnc_sop = "SOP for line-clearnce"
list_hedr_uo_lnclrnc = [hedr_uo_lnclrnc_sop]



######################################################
##  INNERT REPLACEMENT HEADER ITEMS AND OPTIONS     ##
######################################################

                        #>>>>>>>>>>Detail table header items and list thereof <<<<<<<<<<<<<<

hedr_uo_innert_gas = "Innert Gas"
"""Detail header item: Innert gas used for replacement"""
hedr_uo_innert_neg_press = "Negative Press (MPaG)"
"""Detail header item: Negative pressure before innert gas compensation"""
hedr_uo_innert_num_repeat = "Repetition"
"""Detail header item: Times the replacement (vaccum then compensation) repeated"""
list_hedr_uo_innert = [hedr_uo_innert_gas, hedr_uo_innert_neg_press, hedr_uo_innert_num_repeat]
"""Detail header list: List of header items for detail input form for innert gas relacement"""


        #>>>>>>>>>>Option items, lists, and a dictionary for drop-down list in detail input form<<<<<<<<<<<<<<

opt_uo_innert_gas_N2 = "N2"
"""Drop-down option item: choice of gas for innertization. Nitrogen gas"""
opt_uo_innert_gas_Ar = "Ar"
"""Drop-down option item: choice of gas for innertization. Argon gas"""
opt_uo_innert_gas_plchldr = "(placeholder)"
"""Drop-down option item: choice of gas for innertization. Placeholer"""
list_opt_uo_innert_gas = [opt_uo_innert_gas_N2,
                          opt_uo_innert_gas_Ar,
                          opt_uo_innert_gas_plchldr]
"""List for a drop-down list in the detail input table"""

dict_opt_uo_innert = {hedr_uo_innert_gas : list_opt_uo_innert_gas}
"""Dictionary for drop-down lists in detail input form"""

######################################################
##      TEMPR_ HEADER ITEMS AND OPTIONS      ##
######################################################

                        #>>>>>>>>>>Detail table header items and list thereof <<<<<<<<<<<<<<
#hedr_<unit operation>_<parameter> = str
#list_heder_<unit operation> = [<header item 0>,<header item 1>,...]
hedr_uo_tempr_ctrl_mode = "Control Mode"
"""Detail heder item: temperature control mode (e.g. Ti, Ti/Tj, amping)"""
hedr_uo_tempr_ctrl_Ti_sp = "Ti set point (degC)"
"""Detail heder item: Ti set point for Ti, Ti/Tj mode"""
hedr_uo_tempr_ctrl_Ti_limit_low = "Ti low (degC)"
"""Detail heder item: Ti SPEC lower limit designaetd by the process owner."""
hedr_uo_tempr_ctrl_Ti_limit_high = "Ti high (degC)"
"""Detail heder item: Ti SPEC upper limit designated by the process owner."""
hedr_uo_tempr_ctrl_Ti_tgt_low = "Ti tgt low (degC)"
"""Detail heder item: Ti TARGET lower limit designated by the process owner."""
hedr_uo_tempr_ctrl_Ti_tgt_high = "Ti tgt high (degC)"
"""Detail heder item: Ti TARGET higher limit designated by the process owner."""
hedr_uo_tempr_ctrl_Tj_sp = "Tj set point (degC)"
"""Detail heder item: Tj set point for Tj mode"""
hedr_uo_tempr_ctrl_Tj_limit_low = "Tj min (degC)"
"""Detail heder item: Tj lower limit for Tj, Ti/Tj mode."""
hedr_uo_tempr_ctrl_Tj_limit_high = "Tj max (degC)"
"""Detail heder item: Tj higher limit for Tj, Ti/Tj mode"""
hedr_uo_tempr_ctrl_prog_time_val = "Prog. time value"
"""Detail heder item: Ramp up/down time value"""
hedr_uo_tempr_ctrl_prog_time_unit = "Prog. time unit"
"""Detail heder item: Ramp up/down time unit"""
hedr_uo_tempr_ctrl_endpoint_check = "Check end point?"
"""Detail heder item: need for heating/cooling end point check."""

list_hedr_uo_tempr_ctrl = [hedr_uo_tempr_ctrl_mode,
                           hedr_uo_tempr_ctrl_Ti_sp,
                           hedr_uo_tempr_ctrl_Ti_limit_low,
                           hedr_uo_tempr_ctrl_Ti_limit_high,
                           hedr_uo_tempr_ctrl_Ti_tgt_low,
                           hedr_uo_tempr_ctrl_Ti_tgt_high,
                           hedr_uo_tempr_ctrl_Tj_sp,
                           hedr_uo_tempr_ctrl_Tj_limit_low,
                           hedr_uo_tempr_ctrl_Tj_limit_high,
                           #hedr_uo_tempr_ctrl_Ti_tgt_ini,
                           #hedr_uo_tempr_ctrl_prog_Ti_sp_end,
                           hedr_uo_tempr_ctrl_prog_time_val,
                           hedr_uo_tempr_ctrl_prog_time_unit,
                           hedr_uo_tempr_ctrl_endpoint_check]
"""List of header items for unit operation temperature controle"""


        #>>>>>>>>>>Option items, lists, and a dictionary for drop-down list in detail input form<<<<<<<<<<<<<<

#For hedr_uo_tempr_ctrl_mode
opt_uo_tempr_ctrl_mode_TiTj = "Ti/Tj control"
"""Option for detail table: temperature control with single point Ti and Tj range"""
opt_uo_tempr_ctrl_mode_Tj = "Tj control"
"""Option for detail table: temperature control on jacket temperature (single point)"""
opt_uo_tempr_ctrl_mode_prog = "Programme"
"""Option for detail table: temperature ramping, cooling or heating with time constraint"""
opt_uo_tempr_ctrl_mode_Ti = "Ti control"
"""Option for detail table: temperature control on liquid temperature (single point)"""

list_opt_uo_tempr_ctrl_mode = [opt_uo_tempr_ctrl_mode_TiTj,
                               opt_uo_tempr_ctrl_mode_Tj,
                               opt_uo_tempr_ctrl_mode_prog,
                               opt_uo_tempr_ctrl_mode_Ti]
"""List of a series of temperature control options"""

list_opt_uo_tempr_ctrl_check_endpoint = list_yesno
"""Options intended to be used to opt-in/out temperature end-point check."""

list_opt_uo_tempr_ctrl_time_unit = list_time_unit
"""Options intended to be used to choose time unit (seconds, minutes, hours)"""

dict_opt_uo_tempr_ctrl = {hedr_uo_tempr_ctrl_mode : list_opt_uo_tempr_ctrl_mode,
                          hedr_uo_tempr_ctrl_endpoint_check : list_opt_uo_tempr_ctrl_check_endpoint,
                          hedr_uo_tempr_ctrl_prog_time_unit : list_opt_uo_tempr_ctrl_time_unit}
"""Dictionary for detail input form for the unit operation uo_tempr_ctrl"""




######################################################
##      UO_AGITATION HEADER ITEMS AND OPTIONS      ##
######################################################

                        #>>>>>>>>>>Detail table header items and list thereof <<<<<<<<<<<<<<

hedr_uo_agitation_spec = "Specification"
"""header item for the unit operation Agitation, the way the rotation rate is specified: specific rpm, guidance rpm, or discretion"""
hedr_uo_agitation_rpm = "Rotation (rpm)"
"""header item for the unit operation Agitation, specific rotation rate"""
hedr_uo_agitation_Ti_min = "Ti_min (deg-C)"
"""header item for the unit operation Agitation, specific Ti_min during agitation, optional"""
hedr_uo_agitation_Ti_max= "Ti_max (deg-C)"
"""header item for the unit operation Agitation, specific Ti_min during agitation, optional"""
hedr_uo_agitation_time_min = "Minimum time"
"""header item for the unit operation Agitation, minimum agitation time, optional"""
hedr_uo_agitation_time_max = "Maximum time"
"""header item for the unit operation Agitation, maximum agitation time, optional"""
hedr_uo_agitation_time_unit = "Time unit"
"""header item for the unit operation Agitation, second, minute, hour, day"""
hedr_uo_agitation_dissolution_check = "Dissolution check"
"""header item for the unit operation Agitation, need for dissolution check. bool"""

list_hedr_uo_agitation = [hedr_uo_agitation_spec,
                          hedr_uo_agitation_rpm,
                          hedr_uo_agitation_Ti_min,
                          hedr_uo_agitation_Ti_max,
                          hedr_uo_agitation_time_min,
                          hedr_uo_agitation_time_max,
                          hedr_uo_agitation_time_unit,
                          hedr_uo_agitation_dissolution_check]
"""List of uo-specific heder items for the unit operation Agitation"""


        #>>>>>>>>>>Option items, lists, and a dictionary for drop-down list in detail input form<<<<<<<<<<<<<<
opt_uo_agitation_spec_specif = "Specific RPM"
"""option for the header item 'spec'. Specific RPM is provided by the user."""
opt_uo_agitation_spec_guide = "Guidance RPM"
"""option for the header item 'spec'. A guidance RPM is provided by the user."""
opt_uo_agitation_spec_arbitrary = "arbitrary"
"""option for the header item 'spec'. Agitation rate is adjuested on the shop floor at the operator's discretion."""
list_opt_uo_agitation_spec = [opt_uo_agitation_spec_specif,
                              opt_uo_agitation_spec_guide,
                              opt_uo_agitation_spec_arbitrary]
"""List of options for the header item agitation_spec"""

list_opt_uo_agitation_time_unit = list_time_unit
"""List of options for the header item agitation_time_unit"""

list_opt_uo_agitation_dissolution_check = list_yesno
"""List of options for the header item agitation_dissolution_check"""


dict_opt_uo_agitation = {hedr_uo_agitation_spec : list_opt_uo_agitation_spec,
                         hedr_uo_agitation_time_unit : list_opt_uo_agitation_time_unit,
                         hedr_uo_agitation_dissolution_check : list_opt_uo_agitation_dissolution_check}


######################################################
##      <TEMPLATE> HEADER ITEMS AND OPTIONS      ##
######################################################

                        #>>>>>>>>>>Detail table header items and list thereof <<<<<<<<<<<<<<
#hedr_<unit operation>_<parameter> = <str>
#list_heder_<unit operation> = [<header item 0>,<header item 1>,...]
hedr_uo_settling_time_min:str = "minimum settling time"
"""header for the unit operation settling: Minimum settling time"""
hedr_uo_settling_time_max:str = "maximum settling time"
"""header for the unit operation settling: Maximum settling time"""
hedr_uo_settling_time_unit:str = "time unit"
"""header for the unit operation settling: Time unit"""
hedr_uo_settling_Ti_min:str = "Ti_min (deg-C)"
"""header for the unit operation settling: Ti min"""
hedr_uo_settling_Ti_max:str = "Ti_max (deg-C)"
"""header for the unit operation settling: Ti max"""
list_hedr_uo_settling: list[str] = [hedr_uo_settling_time_min,
                                    hedr_uo_settling_time_max,
                                    hedr_uo_settling_time_unit,
                                    hedr_uo_settling_Ti_min,
                                    hedr_uo_settling_Ti_max]
"""list of header items for the unit operation settling"""


        #>>>>>>>>>>Option items, lists, and a dictionary for drop-down list in detail input form<<<<<<<<<<<<<<
#opt_<unit operation>_<parameter>_<option> = str
#list_opt_<unit operation>_<parameter> = [<option_0>, <option_1>, ...]
#dict_opt_<unit operation> = {<heder_item1> : <option_list_1), ...}

dict_opt_uo_settling = {hedr_uo_settling_time_unit : list_time_unit}
"""dict of options for heaader items for the unit operation settling"""

######################################################
##      PHASE TRANSFER HEADER ITEMS AND OPTIONS      ##
######################################################

                        #>>>>>>>>>>Detail table header items and list thereof <<<<<<<<<<<<<<
#hedr_<unit operation>_<parameter> = <str>
#list_heder_<unit operation> = [<header item 0>,<header item 1>,...]
hedr_uo_phasedisch_origin = "origin"
"""Header item for uo_phase_discharge: origin of the discarded lower phase, e.g., reaction vessel, etc."""
hedr_uo_phasedisch_via = "via"
"""Header item for uo_phase_discharge: way point of the discarded lower phase, e.g., multiplexker, etc"""
hedr_uo_phasedisch_destin = "destination"
"""Header item for uo_phase_discharge: destination of the discarded lower phase, e.g., wate liqour tank, etc"""

list_hedr_uo_phasedich = [hedr_uo_phasedisch_origin,
                          hedr_uo_phasedisch_via,
                          hedr_uo_phasedisch_destin]
"""list of  hader fields for the unit operation phase discharge"""


        #>>>>>>>>>>Option items, lists, and a dictionary for drop-down list in detail input form<<<<<<<<<<<<<<
#opt_<unit operation>_<parameter>_<option> = str
#list_opt_<unit operation>_<parameter> = [<option_0>, <option_1>, ...]
#dict_opt_<unit operation> = {<heder_item1> : <option_list_1), ...}




######################################################
##     HEADER ITEMS AND OPTIONS FOR EVAPORATION     ##
######################################################

                        #>>>>>>>>>>Detail table header items and list thereof <<<<<<<<<<<<<<
#hedr_<unit operation>_<parameter> = <str>
#list_heder_<unit operation> = [<header item 0>,<header item 1>,...]
hedr_uo_evap_Tj_min = "Tj_min"
"""header item for the unit operation evaporation: Tj lower limit for evaporation"""
hedr_uo_evap_Tj_max = "Tj_max"
"""header item for the unit operation evaporation: Tj higher limit for evaporation"""
hedr_uo_evap_T_brine_cond_min = "Condenser brine temp min"
"""header item for the unit operation evaporation: lower limit of brine temperature for cndenser"""
hedr_uo_evap_T_brine_cond_max = "Condenser brine temp max"
"""header item for the unit operation evaporation: upper limit of brine temperature for cndenser"""
hedr_uo_evap_press_ctrl = "Pressure control"
"""header item for the unit operation evaporation: pressure specification; arbitrary or specific"""
hedr_uo_evap_press_min = "Press_min"
"""header item for the unit operation evaporation: lower limit for the evaporation pressure"""
hedr_uo_evap_press_max = "Press_max"
"""header item for the unit operation evaporation: upper limit for the evaporation pressure"""
hedr_uo_evap_press_unit = "Press unit"
"""header item for the unit operation evaporation: pressure unit for the evaporation"""
hedr_uo_evap_agit_spec = "Agitation spec"
"""header item for the unit operation evaporation: agitation specification; Specific RPM/Guidance RPM/arbitrary"""
hedr_uo_evap_agit_rpm = "Agitation (rpm)"
"""header item for the unit operation evaporation: agitation rate"""
hedr_uo_evap_val_endpoint_spec_min = "End spec min v/w"
"""header item for the unit operation evaporation: minimum spec value for the evaporation end point"""
hedr_uo_evap_val_endpoint_spec_max = "End spec max v/w"
"""header item for the unit operation evaporation: maximum spec value for the evaporation end point"""
hedr_uo_evap_val_endpoint_guide_min = "End guideline min v/w"
"""header item for the unit operation evaporation: minimum guideline value for the evaporation end point"""
hedr_uo_evap_val_endpoint_guide_max = "End guideline max v/w"
"""header item for the unit operation evaporation: maximum guideline value for the evaporation end point"""

list_hedr_uo_evap = [hedr_uo_evap_Tj_min,
                     hedr_uo_evap_Tj_max,
                     hedr_uo_evap_T_brine_cond_min,
                     hedr_uo_evap_T_brine_cond_max,
                     hedr_uo_evap_press_ctrl,
                     hedr_uo_evap_press_min,
                     hedr_uo_evap_press_max,
                     hedr_uo_evap_press_unit,
                     hedr_uo_evap_agit_spec,
                     hedr_uo_evap_agit_rpm,
                     hedr_uo_evap_val_endpoint_spec_min,
                     hedr_uo_evap_val_endpoint_spec_max,
                     hedr_uo_evap_val_endpoint_guide_min,
                     hedr_uo_evap_val_endpoint_guide_max]
"""list of header fields for the uo_evap"""





        #>>>>>>>>>>Option items, lists, and a dictionary for drop-down list in detail input form<<<<<<<<<<<<<<
#opt_<unit operation>_<parameter>_<option> = str
#list_opt_<unit operation>_<parameter> = [<option_0>, <option_1>, ...]
#dict_opt_<unit operation> = {<heder_item1> : <option_list_1), ...}

opt_uo_evap_press_ctrl_specific = "Specific pressure"
"""option item for the attribute paress_spec_ for uo_evap: Specific pressure value"""
opt_uo_evap_press_ctrl_arbitrary_with_guide = "Arbitrary with optional guideline"
"""option item for the attribute press_spec for uo_evap: Arbitrary with optional guideline"""
opt_uo_evap_press_ctrl_arbitrary = "Arbitrary"
"""option item for the attribute press_spec for uo_evap: Arbitrary without a guieline"""
opt_uo_evap_press_ctrl_full_vac = "Full vacuum (FV)"
"""option item for the attribute press_spec for uo_evap: Full vacuum."""
list_opt_uo_evap_press_ctrl = [opt_uo_evap_press_ctrl_specific,
                               opt_uo_evap_press_ctrl_arbitrary_with_guide,
                               opt_uo_evap_press_ctrl_arbitrary,
                               opt_uo_evap_press_ctrl_full_vac]
"""List of options for the parameter press_spec for the unit operation evap"""

opt_uo_evap_press_unit_MPaA = "MPaA"
"""option item for the attribute press_unit for uo_evap: MPaA"""
opt_uo_evap_press_unit_kPaA = "kPaA"
"""option item for the attribute press_unit for uo_evap: kPaA"""
opt_uo_evap_press_unit_MPaG = "MPaG"
"""option item for the attribute press_unit for uo_evap: MPaG"""
opt_uo_evap_press_unit_kPaG = "kPaG"
"""option item for the attribute press_unit for uo_evap: kPaG"""
list_opt_uo_evap_press_unit = [opt_uo_evap_press_unit_MPaA,
                               opt_uo_evap_press_unit_kPaA,
                               opt_uo_evap_press_unit_MPaG,
                               opt_uo_evap_press_unit_kPaG]

opt_uo_evap_agit_spec_specif = "Specific RPM"
"""option item for the attribute agitation spec for uo_evap: A specific RPM is provided by the user"""
opt_uo_evap_agit_spec_guide = "Guidance RPM"
"""option item for the attribute agitation spec for uo_evap: A guidance RPM is provided by the user"""
opt_uo_evap_agit_spec_arbitrary = "arbitrary RPM"
"""option item for the attribute agitation spec for uo_evap: Totally discretional RPM for evaporation"""
list_opt_uo_evap_agit_spec = [opt_uo_evap_agit_spec_specif,
                              opt_uo_evap_agit_spec_guide,
                              opt_uo_evap_agit_spec_arbitrary]
"""list of option items for agitation for up evap"""


"""list of options for the parameter press_unit for uo_evap"""

# opt_uo_evap_endpoint_unit_L = "L"
# """option item for the attribute endpoint_unit for uo_evap: litre"""
# opt_uo_evap_endpoint_unit_vw = "v/w"
# """option item for the attribute endpoint_unit for uo_evap: v/w"""
# list_opt_up_evap_endpoint_unit = [opt_uo_evap_endpoint_unit_L,
#                                   opt_uo_evap_endpoint_unit_vw]
# """list of options for the parameter endpoint_unit for uo_evap"""

dict_opt_uo_evap = {hedr_uo_evap_press_ctrl : list_opt_uo_evap_press_ctrl,
                    hedr_uo_evap_press_unit : list_opt_uo_evap_press_unit,
                    hedr_uo_evap_agit_spec : list_opt_uo_evap_agit_spec}


######################################################
##      <TEMPLATE> HEADER ITEMS AND OPTIONS      ##
######################################################

                        #>>>>>>>>>>Detail table header items and list thereof <<<<<<<<<<<<<<
#hedr_<unit operation>_<parameter> = <str>
#list_heder_<unit operation> = [<header item 0>,<header item 1>,...]


        #>>>>>>>>>>Option items, lists, and a dictionary for drop-down list in detail input form<<<<<<<<<<<<<<
#opt_<unit operation>_<parameter>_<option> = str
#list_opt_<unit operation>_<parameter> = [<option_0>, <option_1>, ...]
#dict_opt_<unit operation> = {<heder_item1> : <option_list_1), ...}




###########################################################################################################################################
#                                                              PARTS FOR FLOW SHEETS                                                      #
###########################################################################################################################################

################################################################
#            PARTS FOR FLOW SHEETS: COMMON                     #
################################################################

tag_flow_cmn_rec_time = "tag_flow_cmn_time"
"""Tag for a common flowsheet component to record a point of time some action is taken."""
part_flow_cmn_rec_time_jp = '___:___' 
"""Common flowsheet component to record a point of time some action is taken."""

tag_flow_cmn_rec_sign = "tag_flow_cmn_sign"
"""Tag for a common flowsheet component for a signature"""
part_flow_cmn_rec_sign_jp = '   /  /  _____'
"""Common flowsheet component for a signature"""

tag_flow_cmn_time_unit_second = opt_second
"""Tag for a common flowsheet component for an unit of time: second"""
part_flow_cmn_time_unit_second = "秒"
"""Common flowsheet component for an unit of time: second"""
tag_flow_cmn_time_unit_minute = opt_minute
"""Tag for a common flowsheet component for an unit of time: minute"""
part_flow_cmn_time_unit_minute = "分"
"""Common flowsheet component for an unit of time: minute"""
tag_flow_cmn_time_unit_hour = opt_hour
"""Tag for a common flowsheet component for an unit of time: hour"""
part_flow_cmn_time_unit_hour = "時間"
"""Common flowsheet component for an unit of time: hour"""

dict_jp_part_flow_cmn = {tag_flow_cmn_rec_time : part_flow_cmn_rec_time_jp,
                         tag_flow_cmn_rec_sign : part_flow_cmn_rec_sign_jp,
                         tag_flow_cmn_time_unit_second : part_flow_cmn_time_unit_second,
                         tag_flow_cmn_time_unit_minute : part_flow_cmn_time_unit_minute,
                         tag_flow_cmn_time_unit_hour : part_flow_cmn_time_unit_hour}


################################################################
#            PARTS FOR FLOW SHEET: UO_CHARGING                 #
################################################################
####CHARGING####
# tag_part_flow_chgng_title = "tag_chgng_title"
# part_flow_chgng_title_jp = '仕込み'
"""JP title for charging"""

tag_part_flow_chgng_instr_ini = "tag_chgng_instr_ini"
part_flow_chgng_instr_ini_jp = '仕込み開始'
"""Flowseet component for class Charging. An action item of commencement of charging/dosing"""

tag_part_flow_chgng_instr_end = "tag_chgng_instr_end"
part_flow_chgng_instr_end_jp = '仕込み終了'
"""Flowseet component for class Charging. An action item of end of charging/dosing"""

tag_part_flow_chgng_rec_input = "tag_chgng_rec_input"
part_flow_chgng_rec_input_jp = '仕込み量__________kg'
"""Flowseet component for class Charging. A recording element for dispensed amount"""

tag_part_flow_chgng_rec_lot= "tag_chgng_rec_lot"
part_flow_chgng_rec_lot_jp = 'ロット番号__________'
"""Flowseet component for class Charging. A recording element for the lot number of a material"""

tag_part_flow_chgng_rec_hose = "tag_chgng_rec_hose"
part_flow_chgng_rec_hose_jp ='溶媒用フレキID__________'
"""Flowseet component for class Charging. A recording element for the ID of flexible tube for solvents"""

tag_part_flow_chgng_rec_temprini = "tag_chgng_rec_temprini"
part_flow_chgng_rec_temprini_jp = '開始時内温_______℃'
"""Flowseet component for class Charging. A recording element for initial temperature of a certain action"""

tag_part_flow_chgng_rec_temprmax = "tag_chgng_rec_temprmax"
part_flow_chgng_temprmax_jp = '仕込み時最高内温_______℃'
"""Flowseet component for class Charging. A recording element for the maximum temperature"""

tag_part_flow_chgng_rec_temprmin = "tag_chgng_rec_temprmin"
part_flow_chgng_temprmin_jp = '仕込み時最低内温_______℃'
"""Flowseet component for class Charging. A recording element for the minimum"""

tag_part_flow_chgng_rec_temprend = "tag_chgng_rec_temprend"
part_flow_chgng_temprend_jp = '終了時内温_______℃'
"""Flowseet component for class Charging. A recording element for the terminal temperature"""

tag_part_flow_chgng_rec_cmpltd = "tag_chgng_rec_cmpltd"
part_flow_chgng_cmpltd_jp ='□ 仕込み実施'
"""Flowseet component for class Charging. A check box for complete charging/dosing"""

tag_part_flow_chgng_mthd_liq = opt_uo_chgng_method_liq
part_flow_chgng_mthd_liq_jp = "液体投入口"
"""Flowsheet component for class Charging. Charging through liquid charging port. An ption for Liquid charging."""

tag_part_flow_chgng_mthd_shower = opt_uo_chgng_method_shower
part_flow_chgng_mthd_shower_jp = "常設シャワー"
"""Flowsheet component for class Charging. Charging through the fixed shower. An ption for Liquid charging."""

tag_part_flow_chgng_mthd_prssvesl = opt_uo_chgng_method_prssvesl
part_flow_chgng_mthd_prssvesl_jp = "圧送容器"
"""Flowsheet component for class Charging. Charging from a pressure vessel. An ption for Liquid charging."""

tag_part_flow_chgng_mthd_pwdr = opt_uo_chgng_method_pwdr
part_flow_chgng_mthd_pwdr_jp = "粉体投入口"
"""Flowsheet component for class Charging. Charging through the power port. An ption for powder charging."""

tag_part_flow_chgng_mthd_plchldr = opt_uo_chgng_method_method_plchldr
part_flow_chgng_mthd_plchldr_jp = "<Placeholder: charging method>"
"""Flowsheet component for class Charging. A place holder. An ption for Liquid charging."""

dict_jp_part_flow_chgng ={tag_part_flow_chgng_instr_ini : part_flow_chgng_instr_ini_jp,
                         tag_part_flow_chgng_instr_end : part_flow_chgng_instr_end_jp,
                         tag_part_flow_chgng_rec_input : part_flow_chgng_rec_input_jp,
                         tag_part_flow_chgng_rec_lot : part_flow_chgng_rec_lot_jp,
                         tag_part_flow_chgng_rec_hose : part_flow_chgng_rec_hose_jp,
                         tag_part_flow_chgng_rec_temprini : part_flow_chgng_rec_temprini_jp,
                         tag_part_flow_chgng_rec_temprmax : part_flow_chgng_temprmax_jp,
                         tag_part_flow_chgng_rec_temprmin : part_flow_chgng_temprmin_jp,
                         tag_part_flow_chgng_rec_temprend : part_flow_chgng_temprend_jp,
                         tag_part_flow_chgng_rec_cmpltd : part_flow_chgng_cmpltd_jp,
                         tag_part_flow_chgng_mthd_liq : part_flow_chgng_mthd_liq_jp,
                         tag_part_flow_chgng_mthd_shower : part_flow_chgng_mthd_shower_jp,
                         tag_part_flow_chgng_mthd_prssvesl : part_flow_chgng_mthd_prssvesl_jp,
                         tag_part_flow_chgng_mthd_pwdr : part_flow_chgng_mthd_pwdr_jp,
                         tag_part_flow_chgng_mthd_plchldr : part_flow_chgng_mthd_plchldr_jp}


tag_stc_flow_chgng_qty = "tag_stc_qty"
stc_flow_chgng_qty_err_jp = '{qty}±{err} kg'

tag_stc_flow_chgng_time_min = opt_uo_chgng_timctrl_min
stc_flow_chgng_time_min_jp = '*滴下時間{min}以上'
"""Flowsheet component for class Charging. Charging instruction with minimum time"""

tag_stc_flow_chgng_time_max = opt_uo_chgng_timctrl_max
stc_flow_chgng_time_max_jp = '*滴下時間{max}以内'
"""Flowsheet component for class Charging. Charging instruction with maximum time"""

tag_stc_flow_chgng_time_min_max = opt_uo_chgng_timctrl_min_max
stc_flow_chgng_time_min_max_jp = '*滴下時間{min}～{max}以内'
"""Flowsheet component for class Charging. Charging instruction with minimum and maximum time range"""

tag_stc_flow_chgng_temp_min = opt_uo_chgng_temprctrl_min
stc_flow_chgng_temp_min_jp = "仕込み中内温{min}℃以上"
"""Flowsheet component for class Charging. Charging instruction with lower temeperature limit"""

tag_stc_flow_chgng_temp_max = opt_uo_chgng_temprctrl_max
stc_flow_chgng_temp_max_jp ="仕込み中内温{max}℃以下"
"""Flowsheet component for class Charging. Charging instruction with upper temeperature limit"""

tag_stc_flow_chgng_temp_min_max = opt_uo_chgng_temprctrl_min_max
stc_flow_chgng_temp_min_max_jp = "仕込み中内温{min}～{max}℃"
"""Flowsheet component for class Charging. Charging instruction with temeperature range"""

dict_jp_stcs_flow_chgng = {tag_stc_flow_chgng_qty : stc_flow_chgng_qty_err_jp,
                          tag_stc_flow_chgng_time_min : stc_flow_chgng_time_min_jp,
                          tag_stc_flow_chgng_time_max : stc_flow_chgng_time_max_jp,
                          tag_stc_flow_chgng_time_min_max : stc_flow_chgng_time_min_max_jp,
                          tag_stc_flow_chgng_temp_min : stc_flow_chgng_temp_min_jp,
                          tag_stc_flow_chgng_temp_max : stc_flow_chgng_temp_max_jp,
                          tag_stc_flow_chgng_temp_min_max : stc_flow_chgng_temp_min_max_jp}
"""Language dictionary for instruction SENTENCES with place holders 'min' and/or 'max'. Use str.format()"""



###################################################
#        PARTS FOR UO_PlACEHOLDER                 #
###################################################

"""No parts or dictionary for the unit operation 'placeholder'"""


###################################################
#        PARTS FOR UO_LINE_CLEARANCE            #
###################################################
"""Flowsheet component for flowsheets. Simple ones without a placeholders."""
tag_part_flow_lnclrnc_rec_cmpltd = "line clearance completed"
part_flow_lnclrance_rec_cmpltd_jp = "□ラインクリアランス完了"
dict_jp_part_lnclrnce = {tag_part_flow_lnclrnc_rec_cmpltd : part_flow_lnclrance_rec_cmpltd_jp}

"""Instruction sentences with placeholders etc for flowsheets."""
tag_stc_flow_lnclrnc_instr = "line clearance instruction"
stc_flow_lnclrnc_instr = "{sop}に従ってラインクリアランスを実施する。"
dict_jp_stcs_flow_lnclrnc = {tag_stc_flow_lnclrnc_instr : stc_flow_lnclrnc_instr}


###################################################
#        PARTS FOR INNERT_REPLACEMENT             #
###################################################

        #>>>>>>>>>>>>>> flowsheet compoentns in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<
#sets of:
#tag_part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr> = str
#part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr>_<lang> = str
#Follwed by 
#dict_<lang>_part_flow_<unit operation> = {<tag> : <component loc. lang>}
tag_part_flow_uo_innert_gas_N2 = opt_uo_innert_gas_N2
"""Tag for replacing gas N2 on the flowsheet"""
part_flow_uo_innert_gas_N2_jp = "窒素"
"""Flow sheet part Nitorgen"""
tag_part_flow_uo_innert_gas_Ar = opt_uo_innert_gas_Ar
"""Tag for replacing gas argon on the flowsheet"""
part_flow_uo_innert_gas_Ar_jp = "アルゴン"
"""Flow sheet part argon"""
tag_part_flow_uo_innert_gas_plchldr = opt_uo_innert_gas_plchldr
"""Tag for replacing gas placeholder on the flowsheet"""
part_flow_uo_innert_gas_plchldr_jp = "<gas: placeholder>"
"""Flow sheet part placeholder"""

tag_part_flow_uo_innert_rplace_complete = "replacement complete"
"""tag for innert gas replacement complete check-box"""
part_flow_uo_innert_rplace_complete_jp = "□ 置換実施"
"""Flow sheet part for innert gas replacement complete check-box"""

dict_jp_part_flow_uo_innert = {tag_part_flow_uo_innert_gas_N2 : part_flow_uo_innert_gas_N2_jp,
                                tag_part_flow_uo_innert_gas_Ar : part_flow_uo_innert_gas_Ar_jp,
                                tag_part_flow_uo_innert_gas_plchldr : part_flow_uo_innert_gas_plchldr_jp,
                                tag_part_flow_uo_innert_rplace_complete : part_flow_uo_innert_rplace_complete_jp}
"""JP language dictionary for flowsheet parts for the unit operation innert gas replacement"""



        #>>>>>>>>>>>>>> Template sentences for flow sheets in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<
#tag_stc_<unit operation>_<item> = tag
#stc_stc_<unit operation>_<item>_<lang> = <str with placeholder>
#dict_<lang>_stcs_<unit operation> = {tag : sentence}
"""Language dictionary for instruction SENTENCES with place holders 'min' and/or 'max'. Use str.format()"""

tag_stc_flow_uo_innert_instr = "innert replacement instruction"
"""Tag for the instruction sentence for innert gas replacement, the sentence has 3 placeholders: {press}, {gas}, {rep}"""
stc_flow_uo_innert_instr_jp = "到達内圧目安:{press} MPaG, {gas}置換回数{rep}回"
"""Instruction sentence for innert gas replacement"""
dict_jp_stcs_uo_innert = {tag_stc_flow_uo_innert_instr : stc_flow_uo_innert_instr_jp}



###################################################
#        PARTS FOR <unit operation>               #
###################################################

        #>>>>>>>>>>>>>> flowsheet compoentns in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<

#sets of:
#tag_part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr> = str
#part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr>_<lang> = str
#Follwed by 
#dict_<lang>_part_flow_<unit operation> = {<tag> : <component loc. lang>}
tag_part_flow_tempr_ctrl_title_tempr_config:str = "uo title tempr config"
"""Tag for a flowsheet component: Unit operation title for temperature configuration."""
part_flow_tempr_ctrl_title_tempr_config_jp:str = "温調開始"
"""A flowsheet component: Unit operation title for temperature configuration (not complete heating/cooling)."""
tag_part_flow_tempr_ctrl_title_compl_tempr_ctrl:str = "uo title tempr compl control"
"""Tag for a flowsheet component: Unit operation title for complete temperature control."""
part_flow_tempr_ctrl_title_temp_config_jp:str = "温調"
"""A flowsheet component: Unit operation title for complete temperature control."""
# tag_part_flow_tempr_ctrl_prog_mode:str = "instruct programme temp control mode"
# """Tag for a flowsheet component: Instruction for progremme heating/cooling mode"""
# part_flow_tempr_ctrl_prog_mode_jp:str = "プログラム温調する"
# """A flowsheet component: Instruction for progremme heating/cooling mode"""
tag_part_flow_tempr_ctrl_instr_init_temp_ctrl:str = "instr init temp ctrl"
"""Tag for a flowsheet component: Instruction to activate temperature control."""
part_flow_tempr_ctrl_instr_init_temp_ctrl_jp:str = "温調開始"
"""A flowsheet component: Instruction to activate temperature control."""
tag_part_flow_tempr_ctrl_instr_compl_temp_ctrl:str = "instr complete temp ctrl"
"""Tag for a flowsheet component: Instrction to complete the temperature control."""
part_flow_tempr_ctrl_instr_compl_temp_ctrl_jp:str = "温調完了"
"""A flowsheet component: Instrction to complete the temperature control."""
tag_part_flow_tempr_ctrl_instr_check_Ti_in_range:str = "instr check temp in range"
"""Tag for a flowsheet component: Instrction to check if the Ti is in range."""
part_flow_tempr_ctrl_instr_check_Ti_in_range_jp:str = "内温管理範囲内確認"
"""A flowsheet component: Instrction to check if the Ti is in range."""
tag_part_flow_tempr_ctrl_check_config:str = "check temp config"
"""Tag for a flowsheet part: check-box for temperature configuration."""
part_flow_tempr_ctrl_check_config_jp:str = "□ 設定値確認"
"""A flow sheet part: check-box for temperature configuration."""
tag_part_flow_tempr_ctrl_check_activate:str = "check temp control activated"
"""Tag for a flowsheet part: check-box for activation of temperature control."""
part_flow_tempr_ctrl_check_activate_jp:str = "□ 温調開始"
"""A flow sheet part: check-box for activation of temperature control."""
tag_part_flow_tempr_ctrl_check_endpoint:str = "check temp end point"
"""Tag for a flowsheet part: check-box for temperature end point"""
part_flow_tempr_ctrl_check_endpoint_jp:str = "□ 温度到達確認"
"""A flow sheet part: check-box for temperature end point (reached)."""
tag_part_flow_tempr_ctrl_rec_Ti_ini:str = "rec Ti_ini"
"""Tag for a flowsheet part: recrd field for initial Ti"""
part_flow_tempr_ctrl_Ti_ini_jp:str = "温調開始時内温_______℃"
"""A flow sheet part: recrd field for initial Ti"""
tag_part_flow_tempr_ctrl_rec_Ti_end:str = "rec Ti_end"
"""Tag for a flowsheet part: recrd field for end Ti"""
part_flow_tempr_ctrl_Ti_end_jp:str = "温調完了時内温_______℃"
"""A flow sheet part: recrd field for end Ti"""


dict_jp_part_flow_tempr_ctrl = {tag_part_flow_tempr_ctrl_title_tempr_config : part_flow_tempr_ctrl_title_tempr_config_jp,
                                tag_part_flow_tempr_ctrl_title_compl_tempr_ctrl : part_flow_tempr_ctrl_title_temp_config_jp,
                                # tag_part_flow_tempr_ctrl_prog_mode : part_flow_tempr_ctrl_prog_mode_jp,
                                tag_part_flow_tempr_ctrl_instr_init_temp_ctrl : part_flow_tempr_ctrl_instr_init_temp_ctrl_jp,
                                tag_part_flow_tempr_ctrl_instr_compl_temp_ctrl : part_flow_tempr_ctrl_instr_compl_temp_ctrl_jp,
                                tag_part_flow_tempr_ctrl_instr_check_Ti_in_range : part_flow_tempr_ctrl_instr_check_Ti_in_range_jp,
                                tag_part_flow_tempr_ctrl_check_config : part_flow_tempr_ctrl_check_config_jp,
                                tag_part_flow_tempr_ctrl_check_activate : part_flow_tempr_ctrl_check_activate_jp,
                                tag_part_flow_tempr_ctrl_check_endpoint : part_flow_tempr_ctrl_check_endpoint_jp,
                                tag_part_flow_tempr_ctrl_rec_Ti_ini : part_flow_tempr_ctrl_Ti_ini_jp,
                                tag_part_flow_tempr_ctrl_rec_Ti_end : part_flow_tempr_ctrl_Ti_end_jp}
"""Japanese language dictionary for flowsheet parts for unit operation temperature control."""


        #>>>>>>>>>>>>>> Template sentences for flow sheets in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<
#tag_stc_<unit operation>_<item> = tag
#stc_stc_<unit operation>_<item>_<lang> = <str with placeholder>
#dict_<lang>_stcs_<unit operation> = {tag : sentence}
"""Language dictionary for instruction SENTENCES with place holders 'min' and/or 'max'. Use str.format()"""

tag_stc_tempr_ctrl_Tj_sp:str = "Tj set point"
"""Tag for an instruction sentence for temperature control. Tj set point."""
stc_tempr_ctrl_Tj_sp_jp:str = "外温設定: {Tj} ℃"
"""Sentence template for temperature control. Tj set point. Includes placeholder{Tj}"""
tag_stc_tempr_ctrl_Ti_Tj_config:str = "Ti/Tj control"
"""Tag for an instruction sentence for temperature control. Ti/Tj configuration."""
stc_tempr_ctrl_Ti_Tj_config_jp:str = "内外温制御: 内温設定{Ti} ℃、外温範囲{Tj_low}～{Tj_high} ℃"
"""Sentence template for temperature control. Ti/Tj configuraiton. Includes placeholder{Ti}, {Tj_low}, and {Tj_high}"""
tag_stc_tempr_ctrl_prog_mode:str = "configure programme mode"
"""Tag for an instruction sentence for temperature control. Programme mode. Includes placeholder{Ti}, {Tj_low}, and {Tj_high}"""
stc_tempr_ctrl_prog_mode_jp:str = "プログラム温調: 内温設定{Ti} ℃、外温範囲{Tj_low}～{Tj_high} ℃"
"""Sentence template for temperature control. Programme mode. Includes placeholder{Ti}, {Tj_low}, and {Tj_high}"""
tag_stc_tempr_ctrl_prog_duration_minimum:str = "minimum duration programme mode"
"""Sentence template for temperature control. Time requirement for programme heating/cooling mode. Includes  placeholders {time_min} and {time_unit}."""
stc_tempr_ctrl_prog_duration_minimum_jp:str = "温調時間: {time_min} {time_unit}以上"
"""Sentence template for temperature control. Time requirement for programme heating/cooling mode. Includes  placeholders {time_min} and {time_unit}."""
tag_stc_tempr_ctrl_Ti_range:str = "Ti range"
"""Tag for an instruction sentence for temperature control. Ti range. Includes placeholder {Ti_low} and {Ti_high}"""
stc_tempr_ctrl_Ti_range_jp:str = "内温管理幅: {Ti_low}～{Ti_high} ℃"
"""Sentence template for temperature control. Ti range. includes placeholder {Ti_low} and {Ti_high}"""
tag_stc_tempr_ctrl_prog_term_Ti_range:str = "Programme mode terminal Ti range"
"""Tag for an instruction sentence for temperature control. Programme mode terminal Ti range. Includes placeholder {Ti_low} and {Ti_high}"""
stc_tempr_ctrl_prog_term_Ti_range_jp:str = "終点内温範囲: {Ti_low}～{Ti_high} ℃"
"""Sentence template for temperature control. Programme mode terminal Ti range. includes placeholder {Ti_low} and {Ti_high}"""
tag_stc_tempr_ctrl_Ti_high_limit_only:str = "Ti upper limit only"
"""Tag for an instruction sentence for temperature control. Ti upper limit only"""
stc_tempr_ctrl_Ti_uo_limit_only_jp:str = "内温管理: {Ti_high} ℃以下"
"""Sentence template for temperature control. Ti upper limit only. includes placeholder {Ti_high}"""
tag_stc_tempr_ctrl_Ti_low_limit_only:str = "Ti lower limit only"
"""Tag for an instruction sentence for temperature control. Ti lower limit only"""
stc_tempr_ctrl_Ti_low_limit_only_jp:str = "内温管理: {Ti_low} ℃以下"
"""Sentence template for temperature control. Ti lower limit only. includes placeholder {Ti_low}"""
tag_stc_tempr_ctrl_Ti_tgt_range:str = "Ti tgt range"
"""Tag for an instruction sentence for temperature control. Ti target range"""
stc_tempr_ctrl_Ti_tgt_range_jp:str = "内温目標幅: {Ti_low}～{Ti_high} ℃"
"""Sentence template for temperature control. Ti target range. includes placeholder {Ti_low} and {Ti_high}"""
tag_stc_tempr_ctrl_Ti_tgt_single:str = "Ti tgt sp"
"""Tag for an instruction sentence for temperature control. Ti target single point"""
stc_tempr_ctrl_Ti_tgt_single_jp:str = "内温目標値: {Ti} ℃"
"""Sentence template for temperature control. Ti target single point. includes placeholder {Ti}"""
tag_stc_tempr_ctrl_Ti_spec_sp_single:str = "Ti spec sp"
"""Tag for an instruction sentence for temperature control. Ti specification single point for Ti mode. Includes placeholder {Ti}"""
stc_tempr_ctrl_Ti_spec_sp_single_jp:str = "内温設定値: {Ti} ℃"
"""Sentence template for temperature control. Ti specification single point for Ti mode. Includes placeholder {Ti}"""
tag_stc_flow_tempr_ctrl_result_duration:str = "duration for temp control (result)"
"""Tag for a record field for temperature control (cooling/heating) duration in a specic time unit. Includes a placeholder {time_unit}"""
stc_flow_tempr_ctrl_result_duration:str = "温調時間: _________{time_unit}"
"""Sentence teomplate for a record field for temperature control (cooling/heating) duration in a specic time unit. Includes a placeholder {time_unit}"""
dict_jp_stcs_tempr_ctrl = {tag_stc_tempr_ctrl_Tj_sp : stc_tempr_ctrl_Tj_sp_jp,
                           tag_stc_tempr_ctrl_Ti_Tj_config : stc_tempr_ctrl_Ti_Tj_config_jp,
                           tag_stc_tempr_ctrl_prog_mode : stc_tempr_ctrl_prog_mode_jp,
                           tag_stc_tempr_ctrl_prog_duration_minimum : stc_tempr_ctrl_prog_duration_minimum_jp,
                           tag_stc_tempr_ctrl_prog_term_Ti_range : stc_tempr_ctrl_prog_term_Ti_range_jp,
                           tag_stc_tempr_ctrl_Ti_range : stc_tempr_ctrl_Ti_range_jp,
                           tag_stc_tempr_ctrl_Ti_high_limit_only : stc_tempr_ctrl_Ti_uo_limit_only_jp,
                           tag_stc_tempr_ctrl_Ti_low_limit_only : stc_tempr_ctrl_Ti_low_limit_only_jp,
                           tag_stc_tempr_ctrl_Ti_tgt_range : stc_tempr_ctrl_Ti_tgt_range_jp,
                           tag_stc_tempr_ctrl_Ti_tgt_single : stc_tempr_ctrl_Ti_tgt_single_jp,
                           tag_stc_tempr_ctrl_Ti_spec_sp_single : stc_tempr_ctrl_Ti_spec_sp_single_jp,
                           tag_stc_flow_tempr_ctrl_result_duration : stc_flow_tempr_ctrl_result_duration}



###################################################
#        PARTS FOR <unit operation>               #
###################################################

        #>>>>>>>>>>>>>> flowsheet compoentns in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<

#sets of:
#tag_part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr> = str
#part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr>_<lang> = str
#Follwed by 
#dict_<lang>_part_flow_<unit operation> = {<tag> : <component loc. lang>}
tag_part_flow_uo_agitation_title_disslnck:str = "agit dissolution check"
"""Tag for a flowsheet component for uo_agitation: title for combined agitation and dissoltion check operation"""
part_flow_uo_agitation_title_disslnck_jp:str = "攪拌・溶解確認"
"""A flowsheet component for uo_agitation: title for combined agitation and dissoltion check operation"""
tag_part_flow_uo_agitation_instr_rpm_arbitrary:str = "rpm_arbitrary"
"""Tag for a flowsheet component for uo_agitation: instruction for totally arbitrary agitation rate"""
part_flow_uo_agitation_instr_rpm_arbitrary_jp:str = "回転数: 現場調整"
"""A flowsheet component for uo_agitation: instruction for totally arbitrary agitation rate"""

tag_part_flow_uo_agitation_rec_rpm_act:str = "rpm_record_act"
"""Tag for a flowsheet component for uo_agitation: record field for agitation rate"""
part_flow_uo_agitation_rec_rpm_act_jp:str = "回転数:_________rpm"
"""A flowsheet component for uo_agitation: record field for agitation rate"""

tag_part_flow_uo_agitation_rec_chk_agit_ini:str = "agit ini"
"""Tag for a flowsheet component for uo_agitation: check box for agitation initiation"""
part_flow_uo_agitation_rec_chk_agit_ini_jp:str = "□ 攪拌開始"
"""A flowsheet component for uo_agitation: check box for agitation initiation"""
tag_part_flow_uo_agitation_rec_Tj_ini:str = "rec Tj ini"
"""Tag for a flowsheet component for uo_agitation: recording field for initial Tj"""
part_flow_uo_agitation_rec_Tj_ini_jp:str = "開始時外温:_________℃"
"""A flowsheet component for uo_agitation: recording field for initial Tj"""
tag_part_flow_uo_agitation_rec_Ti_ini:str = "rec Ti ini"
"""Tag for a flowsheet component for uo_agitation: recording field for initial Ti"""
part_flow_uo_agitation_rec_Ti_ini_jp:str = "開始時内温:_________℃"
"""A flowsheet component for uo_agitation: recording field for initial Ti"""
tag_part_flow_uo_agitation_instr_dissoln_check_visual:str = "instruction dissolution check by visual"
"""Tag for a flowsheet component for uo_agitation: instruction for dissolution chec by visual"""
part_flow_uo_agitation_instr_dissoln_check_visual_jp:str = "溶解確認:目視"
"""A flowsheet component for uo_agitation: instruction for dissolution chec by visual"""
tag_part_flow_uo_agitation_rec_chk_dissoln:str = "check box dissolution"
"""Tag for a flowsheet component for uo_agitation: check box for dissolution"""
part_flow_uo_agitation_rec_chk_dissoln_jp:str = "□ 溶解確認"
"""A flowsheet component for uo_agitation: check box for dissolution"""
tag_part_flow_uo_agitation_rec_final_Tj:str = "rec Tj agitation end"
"""Tag for a flowsheet component for uo_agitation: recording field for final Tj"""
part_flow_uo_agitation_rec_final_Tj_jp:str = "攪拌終了時外温:_________℃"
"""A flowsheet component for uo_agitation: recording field for final Tj"""
tag_part_flow_uo_agitation_rec_final_Ti:str = "rec Ti agitation end"
"""Tag for a flowsheet component for uo_agitation: recording field for final Ti"""
part_flow_uo_agitation_rec_final_Ti_jp:str = "攪拌終了時内温:_________℃"
"""A flowsheet component for uo_agitation: recording field for final Ti"""
tag_part_flow_uo_agitation_rec_dissoln_Tj:str = "rec Tj at complete dissolution"
"""Tag for a flowsheet component for uo_agitation: recording field for Tj at the time of dissolution"""
part_flow_uo_agitation_rec_dissoln_Tj_jp:str = "溶解確認時外温:_________℃"
"""A flowsheet component for uo_agitation: recording field for Tj at the time of dissolution"""
tag_part_flow_uo_agitation_rec_dissoln_Ti:str = "rec Ti at complete dissolution"
"""Tag for a flowsheet component for uo_agitation: recording field for Ti at the time of dissolution"""
part_flow_uo_agitation_rec_dissoln_Ti_jp:str = "溶解確認時内温:_________℃"
"""A flowsheet component for uo_agitation: recording field for Ti at the time of dissolution"""
tag_part_flow_uo_agitation_rec_chk_agit_compl:str = "agit completed"
"""Tag for a flowsheet component for uo_agitation: check box for agitation completion"""
part_flow_uo_agitation_rec_chk_agit_compl_jp:str = "□ 攪拌完了"
"""A flowsheet component for uo_agitation: check box for agitation completion"""

dict_part_flow_uo_agitation_jp = {tag_part_flow_uo_agitation_title_disslnck : part_flow_uo_agitation_title_disslnck_jp,
                                  tag_part_flow_uo_agitation_instr_rpm_arbitrary : part_flow_uo_agitation_instr_rpm_arbitrary_jp,
                                  tag_part_flow_uo_agitation_rec_rpm_act : part_flow_uo_agitation_rec_rpm_act_jp,
                                  tag_part_flow_uo_agitation_rec_chk_agit_ini : part_flow_uo_agitation_rec_chk_agit_ini_jp,
                                  tag_part_flow_uo_agitation_rec_Tj_ini : part_flow_uo_agitation_rec_Tj_ini_jp,
                                  tag_part_flow_uo_agitation_rec_Ti_ini : part_flow_uo_agitation_rec_Ti_ini_jp,
                                  tag_part_flow_uo_agitation_instr_dissoln_check_visual : part_flow_uo_agitation_instr_dissoln_check_visual_jp,
                                  tag_part_flow_uo_agitation_rec_chk_dissoln : part_flow_uo_agitation_rec_chk_dissoln_jp,
                                  tag_part_flow_uo_agitation_rec_final_Tj : part_flow_uo_agitation_rec_final_Tj_jp,
                                  tag_part_flow_uo_agitation_rec_final_Ti : part_flow_uo_agitation_rec_final_Ti_jp,
                                  tag_part_flow_uo_agitation_rec_dissoln_Tj : part_flow_uo_agitation_rec_dissoln_Tj_jp,
                                  tag_part_flow_uo_agitation_rec_dissoln_Ti : part_flow_uo_agitation_rec_dissoln_Ti_jp,
                                  tag_part_flow_uo_agitation_rec_chk_agit_compl : part_flow_uo_agitation_rec_chk_agit_compl_jp}
"""Japanese lanugae dictionary for flowsheet part for the unit operation Agitation"""

        #>>>>>>>>>>>>>> Template sentences for flow sheets in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<
#tag_stc_<unit operation>_<item> = tag
#stc_<unit operation>_<item>_<lang> = <str with placeholder>
#dict_<lang>_stcs_<unit operation> = {tag : sentence}
"""Language dictionary for instruction SENTENCES with place holders 'min' and/or 'max'. Use str.format()"""

tag_stc_flow_uo_agitation_rpm_spec :str = "component_tag_rpm_spec"
"""Tag for a sentence for the unit operation Agitation: instruction for agitation at an specified agitation rate, includes a placeholder {rpm}"""
stc_flow_uo_agitation_rpm_spec_jp :str = "攪拌速度:{rpm}rpm"
"""Sentence for the unit operation Agitation: instruction for agitation at an specified agitation rate, includes a placeholder {rpm}"""
tag_stc_flow_uo_agitation_rpm_guidance :str = "component_tag_rpm_guidance"
"""Tag for a sentence for the unit operation Agitation: instruction for agitation with a guideline rate, includes a placeholder {rpm}"""
stc_flow_uo_agitation_rpm_guidance_jp :str = "攪拌速度:現場調整(目安{rpm}rpm)"
"""Sentence for the unit operation Agitation: instruction for agitation with a guideline rate, includes a placeholder {rpm}"""
tag_stc_flow_uo_agitation_Ti_range :str = "agitation Ti range"
"""Tag for a sentence for the unit operation Agitation: Instrction on temperature range. Includes placeholders {Ti_min} and {Ti_max}"""
stc_flow_uo_agitation_temp_range_jp :str = "内温範囲:{Ti_min}～{Ti_max}℃"
"""Sentence for the unit operation Agitation: Instrction on temperature range. Includes placeholders {Ti_min} and {Ti_max}"""
tag_stc_flow_uo_agitation_Ti_min :str = "agigation Ti minimum" 
"""Tag for a sentence for the unit operation Agitation: Instruction on minimum temperature. Includes placeholder {Ti_min}"""
stc_flow_uo_agitation_temmp_min_jp :str = "内温{Ti_min}以上"
"""Sentence for the unit operation Agitation: Instruction on minimum temperature. Includes placeholder {Ti_min}"""
tag_stc_flow_uo_agitation_Ti_max :str = "agitation Ti max"
"""Tag for a sentence for the unit operation Agitation: Instruction on maximum temperature. Includes placeholder {Ti_max}"""
stc_flow_uo_agitation_temp_max_jp :str = "内温{Ti_min}以下"
"""Sentence for the unit operation Agitation: """
tag_stc_flow_uo_agitation_time_range :str = "agitation time range"
"""Tag for a sentence for the unit operation Agitation: Instruction on agitation time range. Includes placeholders {time_min}, {time_max} , and {time_unit}"""
stc_flow_uo_agitation_time_range_jp :str = "攪拌継続:{time_min}～{time_max} {time_unit}"
"""Sentence for the unit operation Agitation: Instruction on agitation time range. Includes placeholders {time_min}, {time_max}, and {time_unit}"""
tag_stc_flow_uo_agitation_time_min :str = "agitation minimum time"
"""Tag for a sentence for the unit operation Agitation: Instruction on minimum agitation time. Includes placeholders {time_min} and {time_unit}"""
stc_flow_uo_agitation_time_min_jp :str = "攪拌継続:{time_min} {time_unit}以上"
"""Sentence for the unit operation Agitation: Instruction on minimum agitation time. Includes {time_min} and {time_unit}"""
tag_stc_flow_uo_agitation_time_max :str = "agitation maximum time"
"""Tag for a sentence for the unit operation Agitation: Instruction on maximum agitation time. Includes {time_max} and {time_unit}"""
stc_flow_uo_agitation_time_max_jp :str = "攪拌継続:{time_max} {time_unit}以下"
"""Sentence for the unit operation Agitation:  Instruction on maximum agitation time. Includes {time_max} and {time_unit}"""
tag_stc_flow_uo_agitation_time_single_point:str = "agitation time single point"
"""Tag for a sentence for the unit operation Agitation: Instruction on agitation time (single point). Includes a placeholder {time} and {time_unit}"""
stc_flow_uo_agitation_time_single_point_jp :str = "攪拌時間:{time} {time_unit}"
"""Sentence for the unit operation Agitation:  Instruction on maximum agitation time. Includes a placeholder {time} and {time_unit}"""
tag_stc_flow_uo_agitation_rec_duration:str = "record agitation duration"
"""Tag for a sentence for the unit operation Agitation: Record field for agitation duration, includes a placeholder {time_unit}"""
stc_flow_uo_agitation_rec_duration_jp :str = "攪拌時間:_________{time_unit}"
"""Sentence for the unit operation Agitation: Record field for agitation duration, includes a placeholder {time_unit}"""



dict_jp_stcs_uo_agitation = {tag_stc_flow_uo_agitation_rpm_spec : stc_flow_uo_agitation_rpm_spec_jp,
                             tag_stc_flow_uo_agitation_rpm_guidance : stc_flow_uo_agitation_rpm_guidance_jp,
                             tag_stc_flow_uo_agitation_Ti_range : stc_flow_uo_agitation_temp_range_jp,
                             tag_stc_flow_uo_agitation_Ti_min : stc_flow_uo_agitation_temmp_min_jp,
                             tag_stc_flow_uo_agitation_Ti_max : stc_flow_uo_agitation_temp_max_jp,
                             tag_stc_flow_uo_agitation_time_range : stc_flow_uo_agitation_time_range_jp,
                             tag_stc_flow_uo_agitation_time_min : stc_flow_uo_agitation_time_min_jp,
                             tag_stc_flow_uo_agitation_time_max : stc_flow_uo_agitation_time_max_jp,
                             tag_stc_flow_uo_agitation_time_single_point : stc_flow_uo_agitation_time_single_point_jp,
                             tag_stc_flow_uo_agitation_rec_duration : stc_flow_uo_agitation_rec_duration_jp}
"""Japanese language dictionary for sentences for flowsheet for the unit operation Agitation"""

###################################################
#        PARTS FOR SETTLING               #
###################################################

        #>>>>>>>>>>>>>> flowsheet compoentns in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<

#sets of:
#tag_part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr> = str
#part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr>_<lang> = str
#Follwed by 
#dict_<lang>_part_flow_<unit operation> = {<tag> : <component loc. lang>}
tag_part_uo_settling_init_settling = "instr init settling" 
"""Tag for a flowsheet component for the unit operation settling: """
part_uo_settling_init_settling_jp = "静置開始"
"""A flowsheet component for the unit operation settling: """
tag_part_uo_settling_rec_chk_agitator_stop = "check-box agit stop"
"""Tag for a flowsheet component for the unit operation settling: cutting off agitation for settling"""
part_uo_settling_rec_chk_agitator_stop_jp = "□ 攪拌停止" 
"""A flowsheet component for the unit operation settling:cutting off agitation for settling """
tag_part_uo_settling_rec_Tj_ini = "record Tj ini" 
"""Tag for a flowsheet component for the unit operation settling: record field for the initial Tj"""
part_uo_settling_rec_Tj_ini_jp = "静置開始時外温_________℃"
"""A flowsheet component for the unit operation settling: """
tag_part_uo_settling_rec_Ti_ini = "recort Ti ini"
"""Tag for a flowsheet component for the unit operation settling: recorod field for the initial Ti"""
part_uo_settling_rec_Ti_ini_jp =  "静置開始時内温_________℃"
"""A flowsheet component for the unit operation settling: end of settling field for the initial Ti"""
tag_part_uo_settling_end_settling = "instr end settling"
"""Tag for a flowsheet component for the unit operation settling: end of settling"""
part_uo_settling_end_settling = "静置終了" 
"""A flowsheet component for the unit operation settling: end of settling"""
tag_part_uo_settling_Tj_end = "record Tj end"
"""Tag for a flowsheet component for the unit operation settling: Recording field for Tj at the end of settling"""
part_uo_settling_Tj_end_jp = "静置終了時外温_________℃"
"""A flowsheet component for the unit operation settling: Recording field for Tj at the end of settling"""
tag_part_uo_settling_Ti_end = "record Ti end"
"""Tag for a flowsheet component for the unit operation settling:Recording field for Ti at the end of settling """
part_uo_settling_Ti_end_jp = "静置終了時内_________℃"
"""A flowsheet component for the unit operation settling: Recording field for Ti at the end of settling"""

dict_jp_part_flow_uo_settling = {tag_part_uo_settling_init_settling : part_uo_settling_init_settling_jp,
                                tag_part_uo_settling_rec_chk_agitator_stop : part_uo_settling_rec_chk_agitator_stop_jp,
                                tag_part_uo_settling_rec_Tj_ini : part_uo_settling_rec_Tj_ini_jp,
                                tag_part_uo_settling_rec_Ti_ini : part_uo_settling_rec_Ti_ini_jp,
                                tag_part_uo_settling_end_settling : part_uo_settling_end_settling,
                                tag_part_uo_settling_Tj_end : part_uo_settling_Tj_end_jp,
                                tag_part_uo_settling_Ti_end : part_uo_settling_Ti_end_jp}
"""language dictionary for flowsheet components for the unit opeataion settling"""


        #>>>>>>>>>>>>>> Template sentences for flow sheets in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<
#tag_stc_<unit operation>_<item> = tag
#stc_stc_<unit operation>_<item>_<lang> = <str with placeholder>
#dict_<lang>_stcs_<unit operation> = {tag : sentence}
"""Japanese language dictionary for instruction SENTENCES with place holders 'min' and/or 'max'. Use str.format()"""

tag_stc_uo_settling_time_min = "sentence minimum sttling time" 
"""Tag for a flowsheet sentence for the unit operation settling: minimum settling time. contains placeholders {time_min} and {time_unit}"""
part_uo_settling_time_min_jp = "静置時間:{time_min} {time_unit}以上"
"""A flowsheet component for the unit operation settling: minimum settling time. contains placeholders {time_min} and {time_unit}"""
tag_stc_uo_settling_time_max = "sentence maximum sttling time" 
"""Tag for a flowsheet sentence for the unit operation settling: maximum settling time. contains placeholders {time_max} and {time_unit}"""
part_uo_settling_time_max_jp = "静置時間:{time_max} {time_unit}以下"
"""A flowsheet component for the unit operation settling: maximum settling time. contains placeholders {time_max} and {time_unit}"""
tag_stc_uo_settling_time_range = "sentence sttling time range" 
"""Tag for a flowsheet sentence for the unit operation settling: settling time range. contains placeholders {time_min}, {time_max}, and {time_unit}"""
part_uo_settling_time_range_jp = "静置時間:{time_min}～{time_max} {time_unit}"
"""A flowsheet component for the unit operation settling: settling time range. contains placeholders {time_min}, {time_max}, and {time_unit}"""
tag_stc_uo_settling_time_single_point = "sentence sttling single point" 
"""Tag for a flowsheet sentence for the unit operation settling: settling time single point. contains placeholders {time} and {time_unit}"""
part_uo_settling_time_single_point_jp = "静置時間:{time} {time_unit}"
"""A flowsheet component for the unit operation settling:  settling time single point. contains placeholders {time} and {time_unit}"""
tag_stc_uo_settling_Ti_min = "settling Ti min" 
"""Tag for a flowsheet sentence for the unit operation settling: Minimum Ti for settling. contains placeholders {Ti_min}"""
part_uo_settling_Ti_min_jp = "静置時内温:{Ti_min} ℃以上"
"""A flowsheet component for the unit operation settling: Minimum Ti for settling. contains placeholders {Ti_min}"""
tag_stc_uo_settling_Ti_max = "settling Ti max" 
"""Tag for a flowsheet sentence for the unit operation settling: Maximum Ti for settling. contains placeholders {Ti_max}"""
part_uo_settling_Ti_max_jp = "静置時内温:{Ti_max} ℃以下"
"""A flowsheet component for the unit operation settling: Maximum Ti for settling. contains placeholders {Ti_max}"""
tag_stc_uo_settling_Ti_range = "settling Ti range" 
"""Tag for a flowsheet sentence for the unit operation settling: Ti range for settling. contains placeholders {Ti_min} and {Ti_max}"""
part_uo_settling_Ti_range_jp = "静置時内温:{Ti_min}～{Ti_max}℃"
"""A flowsheet component for the unit operation settling: Ti range for settling. contains placeholders {Ti_min} and {Ti_max}"""
tag_stc_uo_settling_rec_duration = "record field settling duration" 
"""Tag for a flowsheet sentence for the unit operation settling: record field for setting duration. contains placeholders {time_unit}"""
part_uo_settling_duration_jp = "静置時間_________{time_unit}"
"""A flowsheet component for the unit operation settling: record field for setting duration. contains placeholders {time_unit}"""
dict_jp_stcs_uo_settling = {tag_stc_uo_settling_time_min : part_uo_settling_time_min_jp,
                            tag_stc_uo_settling_time_max : part_uo_settling_time_max_jp,
                            tag_stc_uo_settling_time_range : part_uo_settling_time_range_jp,
                            tag_stc_uo_settling_time_single_point : part_uo_settling_time_single_point_jp,
                            tag_stc_uo_settling_Ti_min : part_uo_settling_Ti_min_jp,
                            tag_stc_uo_settling_Ti_max : part_uo_settling_Ti_max_jp,
                            tag_stc_uo_settling_Ti_range : part_uo_settling_Ti_range_jp,
                            tag_stc_uo_settling_rec_duration : part_uo_settling_duration_jp}
"""Japanese language dictionary for senteces in flowsheets for the unit operation settling"""

###################################################
#        PARTS FOR <unit operation>               #
###################################################

        #>>>>>>>>>>>>>> flowsheet compoentns in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<

#sets of:
#tag_part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr> = str
#part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr>_<lang> = str
#Follwed by 
#dict_<lang>_part_flow_<unit operation> = {<tag> : <component loc. lang>}
tag_part_flow_uo_phasedisch_method_connection = "line connection"
"""Tag for a flowsheet component for a unit operation phase discharging: Discharging line connection"""
part_flow_uo_phasedisch_method_connection_jp = "ライン構築"
"""A flowsheet component for a unit operation phase discharging: Discharging line connection"""

tag_part_flow_uo_phasedisch_chk_connected = "check box line connected"
"""Tag for a flowsheet component for a unit operation phase discharging: check box for phase discharging line connected"""
part_flow_uo_phasedisch_chk_connected_jp = "□ ライン構築確認"
"""A flowsheet component for a unit operation phase discharging: check box for phase discharging line connected"""

tag_part_flow_uo_phasedisch_method_disch = "instr (method col) disch"
"""Tag for a flowsheet component for a unit operation phase discharging: Instruction (method colum) for discharging."""
part_flow_uo_phasedisch_method_disch_jp = "下層排出"
"""A flowsheet component for a unit operation phase discharging: Instruction (method colum) for discharging."""

tag_part_flow_uo_phasedisch_content_disch = "action (content col) disch"
"""Tag for a flowsheet component for a unit operation phase discharging: Description of action (content column) for discharging"""
part_flow_uo_phasedisch_content_disch_jp = "排出実施"
"""A flowsheet component for a unit operation phase discharging: Description of action (content column) for discharging"""

tag_part_flow_uo_phasedisch_chk_discharged = "check box phase discharged"
"""Tag for a flowsheet component for a unit operation phase discharging: check box for the completion of the phase discharging"""
part_flow_uo_phasedisch_chk_discharged_jp = "□ 実施確認"
"""A flowsheet component for a unit operation phase discharging: check box for the completion of the phase discharging"""

dict_jp_part_flow_uo_phasedisch = {tag_part_flow_uo_phasedisch_method_connection : part_flow_uo_phasedisch_method_connection_jp,
                                   tag_part_flow_uo_phasedisch_chk_connected : part_flow_uo_phasedisch_chk_connected_jp,
                                   tag_part_flow_uo_phasedisch_method_disch : part_flow_uo_phasedisch_method_disch_jp,
                                   tag_part_flow_uo_phasedisch_content_disch : part_flow_uo_phasedisch_content_disch_jp,
                                   tag_part_flow_uo_phasedisch_chk_discharged : part_flow_uo_phasedisch_chk_discharged_jp}
"""Language dictionary for flowsheet parts for the unit operation phase discharging"""


        #>>>>>>>>>>>>>> Template sentences for flow sheets in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<
#tag_stc_<unit operation>_<item> = tag
#stc_stc_<unit operation>_<item>_<lang> = <str with placeholder>
#dict_<lang>_stcs_<unit operation> = {tag : sentence}
"""Japanese language dictionary for instruction SENTENCES with place holders 'min' and/or 'max'. Use str.format()"""

tag_stc_uo_phasedisch_origin = "sentence origin"
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate the origon vessel of the discharged phase, includes placeholder {origin}"""
stc_uo_phasedisch_origin_jp = "移送元: {origin}"
"""A instruction sentence for a unit operation phase discharging: sentence to designate the origon vessel of the discharged phase, includes placeholder {origin}"""
tag_stc_uo_phasedisch_via = "sentence vis"
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate the way point, e.g., multiplexer, includes placeholder {via}"""
stc_uo_phasedisch_via_jp = "経由: {via}"
"""A instruction sentence for a unit operation phase discharging: sentence to designate the way point, e.g., multiplexer, includes placeholder {via}"""
tag_stc_uo_phasedisch_destin_single = "sentence single destination"
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate the destination, includes placeholder {destination}"""
stc_uo_phasedisch_destin_single_jp = "移送先: {destination}"
"""A instruction sentence for a unit operation phase discharging: sentence to designate the destination, includes placeholder {destination}"""
tag_stc_uo_phasedisch_destin_multi = "sentence multiple destination"
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate multiple destinations, includes placeholder {destination}--singular!"""
stc_uo_phasedisch_destin_multi_jp = "移送先: {destination} (使用したものを〇)"
"""A instruction sentence for a unit operation phase discharging: sentence to designate multiple destinations, includes placeholder {destination}--singular!"""
dict_jp_stcs_uo_phasedisch = {tag_stc_uo_phasedisch_origin : stc_uo_phasedisch_origin_jp,
                              tag_stc_uo_phasedisch_via : stc_uo_phasedisch_via_jp,
                              tag_stc_uo_phasedisch_destin_single : stc_uo_phasedisch_destin_single_jp,
                              tag_stc_uo_phasedisch_destin_multi : stc_uo_phasedisch_destin_multi_jp}
"""Japanese language dictionary for instruction sentences for the unit operation phase discharging"""

###################################################
#        PARTS FOR <unit operation>               #
###################################################

        #>>>>>>>>>>>>>> flowsheet compoentns in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<

#sets of:
#tag_part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr> = str
#part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr>_<lang> = str
#Follwed by 
#dict_<lang>_part_flow_<unit operation> = {<tag> : <component loc. lang>}

tag_part_flow_uo_evap_method_ini = "method col init evap"
"""the tag for a flowhsheet component for uo_evap: a sub title to commense evaporation in the method column"""
part_flow_uo_evap_method_ini_jp = "濃縮開始"
"""A flowhsheet component for uo_evap: a sub title to commense evaporation in the method column"""

tag_part_flow_uo_evap_instr_chronol_rec = "instr chronological record"
"""the tag for a flowhsheet component for uo_evap: instruction to take a chronological record"""
part_flow_uo_evap_instr_chronol_rec_jp = "*詳細記録は経時的な作業記録書に記載する。"
"""A flowhsheet component for uo_evap: instruction to take a chronological record"""

tag_part_flow_uo_evap_Tj_artibrary = "evap Tj arbitrary"
"""the tag for a flowhsheet component for uo_evap: instruction for arbitrary Tj for evaporation"""
part_flow_uo_evap_Tj_artibrary_jp = "外温設定: 現場調整"
"""A flowhsheet component for uo_evap: instruction for arbitrary Tj for evaporation"""

tag_part_flow_uo_evap_T_brine_artibrary = "evap brine temp arbitrary"
"""the tag for a flowhsheet component for uo_evap: instruction for arbitrary brine temperature for evaporation"""
part_flow_uo_evap_T_brine_artibrary_jp = "冷却用ブライン: 現場調整"
"""A flowhsheet component for uo_evap: instruction for arbitrary brine temperature for evaporation"""

tag_part_flow_uo_evap_pres_arbitrary = "evap vacuum arbitrary"
"""the tag for a flowhsheet component for uo_evap: instruction for arbitrary pressure for evaporation"""
part_flow_uo_evap_pres_arbitrary_jp = "真空度:現場調整"
"""A flowhsheet component for uo_evap: instruction for arbitrary pressure for evaporation"""

tag_part_flow_uo_evap_pres_full_vac = "evap full vacuum"
"""the tag for a flowhsheet component for uo_evap: instruction for full vacuume for evaporation"""
part_flow_uo_evap_pres_full_vac_jp = "真空度: FV"
"""A flowhsheet component for uo_evap: instruction for full vacuume for evaporation"""

tag_part_flow_uo_evap_agitation_arbitray = "evap agitation arbitrary"
"""the tag for a flowhsheet component for uo_evap: agitation at an arbitrary rotation"""
part_flow_uo_evap_agitation_arbitrary_jp = "攪拌数:現場調整"
"""A flowhsheet component for uo_evap: agitation at an arbitrary rotation"""

tag_part_flow_uo_evap_method_end = "evaporation end"
"""the tag for a flowhsheet component for uo_evap: end of evaporation"""
part_flow_uo_evap_method_end_jp = "終了"
"""A flowhsheet component for uo_evap: end of evaporation"""

tag_part_flow_uo_evap_rec_Tj_sp = "recorod Tj set point"
"""the tag for a flowhsheet component for uo_evap: record field for Tj"""
part_flow_uo_evap_rec_Tj_sp_jp = "外温設定__________℃"
"""A flowhsheet component for uo_evap: record field for Tj"""

tag_part_flow_uo_evap_rec_T_brine_sp = "record brine temp"
"""the tag for a flowhsheet component for uo_evap: record field for brine temperature"""
part_flow_uo_evap_rec_T_brine_sp_jp = "冷却ブライン__________℃"
"""A flowhsheet component for uo_evap: record field for brine temperature"""

tag_part_flow_uo_evap_rec_rpm = "record rpm"
"""the tag for a flowhsheet component for uo_evap: record field for agitation rate"""
part_flow_uo_evap_rec_rpm_jp = "攪拌数__________rpm"
"""A flowhsheet component for uo_evap: record field for agitation rate"""

tag_part_flow_uo_evap_rec_Ti_ini = "reocord Ti ini"
"""the tag for a flowhsheet component for uo_evap: recorod field for Ti at the beginning of evaporation"""
part_flow_uo_evap_rec_Ti_ini_jp = "濃縮開始時内温__________℃"
"""A flowhsheet component for uo_evap: recorod field for Ti at the beginning of evaporation"""

tag_part_flow_uo_evap_rec_Ti_max = "record Ti max"
"""the tag for a flowhsheet component for uo_evap: record field for the maximum Ti during evaporation"""
part_flow_uo_evap_rec_Ti_max_jp = "濃縮時最高内温__________℃"
"""A flowhsheet component for uo_evap: record field for the maximum Ti during evaporation"""

tag_part_flow_uo_evap_rec_Ti_end = "record Ti end"
"""the tag for a flowhsheet component for uo_evap: record field for the Ti at the end"""
part_flow_uo_evap_rec_Ti_end_jp = "濃縮終了時内温__________℃"
"""A flowhsheet component for uo_evap: record field for the Ti at the end"""

tag_part_flow_uo_evap_rec_vol_end = "record vol end"
"""the tag for a flowhsheet component for uo_evap: record field for the volume (L) at the end"""
part_flow_uo_evap_rec_vol_end_jp = "濃縮終了時液量:約__________L"
"""A flowhsheet component for uo_evap: record field for the volume (L) at the end"""

dict_jp_part_flow_uo_evap = {tag_part_flow_uo_evap_method_ini : part_flow_uo_evap_method_ini_jp,
                             tag_part_flow_uo_evap_instr_chronol_rec : part_flow_uo_evap_instr_chronol_rec_jp,
                             tag_part_flow_uo_evap_Tj_artibrary : part_flow_uo_evap_Tj_artibrary_jp,
                             tag_part_flow_uo_evap_T_brine_artibrary : part_flow_uo_evap_T_brine_artibrary_jp,
                             tag_part_flow_uo_evap_pres_arbitrary : part_flow_uo_evap_pres_arbitrary_jp,
                             tag_part_flow_uo_evap_agitation_arbitray : part_flow_uo_evap_agitation_arbitrary_jp,
                             tag_part_flow_uo_evap_pres_full_vac : part_flow_uo_evap_pres_full_vac_jp,
                             tag_part_flow_uo_evap_method_end : part_flow_uo_evap_method_end_jp,
                             tag_part_flow_uo_evap_rec_Tj_sp : part_flow_uo_evap_rec_Tj_sp_jp,
                             tag_part_flow_uo_evap_rec_T_brine_sp : part_flow_uo_evap_rec_T_brine_sp_jp,
                             tag_part_flow_uo_evap_rec_rpm : part_flow_uo_evap_rec_rpm_jp,
                             tag_part_flow_uo_evap_rec_Ti_ini : part_flow_uo_evap_rec_Ti_ini_jp,
                             tag_part_flow_uo_evap_rec_Ti_max : part_flow_uo_evap_rec_Ti_max_jp,
                             tag_part_flow_uo_evap_rec_Ti_end : part_flow_uo_evap_rec_Ti_end_jp,
                             tag_part_flow_uo_evap_rec_vol_end : part_flow_uo_evap_rec_vol_end_jp}
"""Japanese language dictionary for flowsheet components for the unit operation evaporation"""



        #>>>>>>>>>>>>>> Template sentences for flow sheets in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<
#tag_stc_<unit operation>_<item> = tag
#stc_stc_<unit operation>_<item>_<lang> = <str with placeholder>
#dict_<lang>_stcs_<unit operation> = {tag : sentence}
"""Language dictionary for instruction SENTENCES with place holders 'min' and/or 'max'. Use str.format()"""

tag_stc_flow_uo_evap_Tj_range = "evap Tj range"
"""the tag for a sentence for component for uo_evap: Tj range for evaporation, includes placeholders {Tj_min} and {Tj_max}"""
stc_flow_uo_evap_Tj_range_jp = "外温範囲:{Tj_min}～{Tj_max}℃"
"""A sentence for uo_evap: tag for Tj range for evaporation; includes placeholders {Tj_min} and {Tj_max}"""
tag_stc_flow_uo_evap_Tj_min = "evap Tj min"
"""the tag for a sentence for component for uo_evap: minimum Tj for evaporation; includes placeholders {Tj_min}"""
stc_flow_uo_evap_Tj_min_jp = "外温{Tj_min}℃以上"
"""A sentence for uo_evap: tag for minimum Tj; includes placeholders {Tj_min}"""
tag_stc_flow_uo_evap_Tj_max = "evap Tj max"
"""the tag for a sentence for component for uo_evap: maximum Tj for evaporation; includes placeholders {Tj_max}"""
stc_flow_uo_evap_Tj_max_jp = "外温{Tj_max}℃以下"
"""A sentence for uo_evap: maximum Tj for evaporation; includes placeholders {Tj_max}"""

tag_stc_flow_uo_evap_T_brine_range = "evap T_brine range"
"""the tag for a sentence for component for uo_evap: T_brine range for evaporation, includes placeholders {Tbr_min} and {Tbr_max}"""
stc_flow_uo_evap_T_brine_range_jp = "ブライン温度範囲:{Tbr_min}～{Tbr_max}℃"
"""A sentence for uo_evap: tag for T_brine range for evaporation; includes placeholders {Tbr_min} and {Tbr_max}"""
tag_stc_flow_uo_evap_T_brine_min = "evap T_brine min"
"""the tag for a sentence for component for uo_evap: minimum T_brine for evaporation; includes placeholders {Tbr_min}"""
stc_flow_uo_evap_T_brine_min_jp = "ブライン温度{Tbr_min}℃以上"
"""A sentence for uo_evap: tag for minimum T_brine; includes placeholders {Tbr_min}"""
tag_stc_flow_uo_evap_T_brine_max = "evap T_brine max"
"""the tag for a sentence for component for uo_evap: maximum T_brine for evaporation; includes placeholders {Tbr_max}"""
stc_flow_uo_evap_T_brine_max_jp = "ブライン温度{Tbr_max}℃以下"
"""A sentence for uo_evap: maximum T_brine for evaporation; includes placeholders {Tbr_max}"""

tag_stc_flow_uo_evap_press_spec_range = "evap press range"
"""the tag for a sentence for component for uo_evap: instruction for pressure range; includes placeholders {P_min}, {P_max}, {P_unit}"""
stc_flow_uo_evap_press_spec_range_jp = "真空度:{P_min}～{P_max} {P_unit}"
"""A sentence for uo_evap: instruction for pressure range; includes placeholders {P_min}, {P_max}, {P_unit}"""
tag_stc_flow_uo_evap_press_spec_min = "evap press minimum"
"""the tag for a sentence for component for uo_evap: instruction for minimum pressure; includes placeholders {P_min} and {P_unit}"""
stc_flow_uo_evap_press_spec_min_jp = "真空度:{P_min} {P_unit}以上"
"""A sentence for uo_evap: instruction for minimum pressure; includes placeholders {P_min} and {P_unit}"""
tag_stc_flow_uo_evap_press_spec_max = "evap press maximum"
"""the tag for a sentence for component for uo_evap: instruction for maximum pressure; includes placeholders {P_max} and {P_unit}"""
stc_flow_uo_evap_press_spec_max_jp = "真空度:{P_max} {P_unit}以下"
"""A sentence for uo_evap: instruction for maximum pressure; includes placeholders {P_max} and {P_unit}"""


tag_stc_flow_uo_evap_press_guide_range = "evap press guideline range"
"""the tag for a sentence for component for uo_evap: guideline for pressure range; includes placeholders {P_min}, {P_max}, {P_unit}"""
stc_flow_uo_evap_press_guide_range_jp = "真空度:現場調整(目安{P_min}～{P_max} {P_unit})"
"""A sentence for uo_evap:guideline for pressure range; includes placeholders {P_min}, {P_max}, {P_unit}"""
tag_stc_flow_uo_evap_press_guide_singlepoint= "evap press guideline single point"
"""the tag for a sentence for component for uo_evap: guideline for a single point pressure; includes placeholders {P}, {P_unit}"""
stc_flow_uo_evap_press_guide_singlepoint_jp = "真空度:現場調整(目安{P} {P_unit})"
"""A sentence for uo_evap:guideline for a single point pressure; includes placeholders {P}, {P_unit}"""
tag_stc_flow_uo_evap_press_guide_min = "evap press guideline minimum"
"""the tag for a sentence for component for uo_evap: guideline for minimum pressure; includes placeholders {P_min} and {P_unit}"""
stc_flow_uo_evap_press_guide_min_jp = "真空度:現場調整(目安{P_min} {P_unit}以上)"
"""A sentence for uo_evap: guideline for minimum pressure; includes placeholders {P_min} and {P_unit}"""
tag_stc_flow_uo_evap_press_guide_max = "evap press guideline maximum"
"""the tag for a sentence for component for uo_evap: guideline for maximum pressure; includes placeholders {P_max} and {P_unit}"""
stc_flow_uo_evap_press_guide_max_jp = "真空度:現場調整(目安{P_max} {P_unit}以下)"
"""A sentence for uo_evap: guideline for maximum pressure; includes placeholders {P_max} and {P_unit}"""

tag_stc_flow_uo_evap_agitation_spec = "evap agitation spec"
"""the tag for a sentence for component for uo_evap: agitation at a specific agitation rate; includes placeholders {rpm}"""
stc_flow_uo_evap_agitation_spec_jp = "攪拌速度:{rpm}rpm"
"""A sentence for uo_evap: agitation at a specific agitation rate; includes placeholders {rpm}"""
tag_stc_flow_uo_evap_agitation_arbitrary_with_guide = "evap agitation arbitrary with guide"
"""the tag for a sentence for component for uo_evap: agitation at a specific agitation rate; includes placeholders {rpm}"""
stc_flow_uo_evap_agitation_arbitrary_with_guide_jp = "攪拌速度:現場調整(目安{rpm}rpm)"
"""A sentence for uo_evap: agitation at a specific agitation rate; includes placeholders {rpm}"""

tag_stc_flow_uo_evap_endpoint_spec_range = "evap endpoint spec range"
"""the tag for a sentence for component for uo_evap: instruction for the evaporation endpoint; includes placeholders {L_min}, {L_max}, {vw_min}, {vw_max}"""
stc_flow_uo_evap_endpoint_spec_range_jp = "終点:{L_min}～{L_max} L ({vw_min}～{vw_max} v/w)"
"""A sentence for uo_evap: instruction for the evaporation endpoint; includes placeholders {L_min}, {L_max}, {vw_min}, {vw_max}"""
tag_stc_flow_uo_evap_endpoint_spec_min = "evap endpoint spec min"
"""the tag for a sentence for component for uo_evap: instruction for minimum spec endpoint; includes placeholders {L_min}, {vw_min}"""
stc_flow_uo_evap_endpoint_spec_min_jp = "終点:{L_min} L以上 ({vw_min} v/w)"
"""A sentence for uo_evap: instruction for minimum spec endpoint; includes placeholders {L_min}, {vw_min}"""
tag_stc_flow_uo_evap_endpoint_spec_max = "evap endpoint spec max"
"""the tag for a sentence for component for uo_evap: instruction for maximum spec endpoint; includes placeholders {L_max}, {vw_max}"""
stc_flow_uo_evap_endpoint_spec_max_jp = "終点:{L_max} L以下 ({vw_max} v/w)"
"""A sentence for uo_evap: instruction for maximum spec endpoint; includes placeholders {L_max}, {vw_max}"""

tag_stc_flow_uo_evap_endpoint_guide_range = "evap endpoint guideline range"
"""the tag for a sentence for component for uo_evap: instruction for the evaporation endpoint; includes placeholders {L_min}, {L_max}, {vw_min}, {vw_max}"""
stc_flow_uo_evap_endpoint_guide_range_jp = "終点目安:{L_min}～{L_max} L ({vw_min}～{vw_max} v/w)"
"""A sentence for uo_evap: instruction for the evaporation endpoint; includes placeholders {L_min}, {L_max}, {vw_min}, {vw_max}"""
tag_stc_flow_uo_evap_endpoint_guide_single = "evap endpoint guideline single point"
"""the tag for a sentence for component for uo_evap: instruction for the evaporation single point endpoint; includes placeholders {L_single}, {vw_single}"""
stc_flow_uo_evap_endpoint_guide_single_jp = "終点目安:{L_single} L ({vw_single} v/w)"
"""A sentence for uo_evap: instruction for the evaporation single point endpoint; includes placeholders {L_min}, {L_max}, {vw_min}, {vw_max}"""
tag_stc_flow_uo_evap_endpoint_guide_min = "evap endpoint guideline min"
"""the tag for a sentence for component for uo_evap: instruction for minimum guideline endpoint; includes placeholders {L_min}, {vw_min}"""
stc_flow_uo_evap_endpoint_guide_min_jp = "終点目安:{L_min} L以上 ({vw_min} v/w)"
"""A sentence for uo_evap: instruction for minimum guideline endpoint; includes placeholders {L_min}, {vw_min}"""
tag_stc_flow_uo_evap_endpoint_guide_max = "evap endpoint guideline max"
"""the tag for a sentence for component for uo_evap: instruction for maximum guideline endpoint; includes placeholders {L_max}, {vw_max}"""
stc_flow_uo_evap_endpoint_guide_max_jp = "終点目安:{L_max} L以下 ({vw_max} v/w)"
"""A sentence for uo_evap: instruction for maximum guideline endpoint; includes placeholders {L_max}, {vw_max}"""

tag_stc_flow_uo_evap_rec_press = "record field for evaporation pressure/vacuum"
"""the tag for a sentence for component for uo_evap: recording field for vacuum; includes placeholders {P_unit}"""
stc_flow_uo_evap_rec_vacuum_jp = "真空度__________{P_unit}"
"""A sentence for uo_evap: recording field for vacuum; includes placeholders {P_unit}"""

dict_jp_stcs_flow_uo_evap = {tag_stc_flow_uo_evap_Tj_range : stc_flow_uo_evap_Tj_range_jp,
                                tag_stc_flow_uo_evap_Tj_min : stc_flow_uo_evap_Tj_min_jp,
                                tag_stc_flow_uo_evap_Tj_max : stc_flow_uo_evap_Tj_max_jp,
                                tag_stc_flow_uo_evap_T_brine_range : stc_flow_uo_evap_T_brine_range_jp,
                                tag_stc_flow_uo_evap_T_brine_min : stc_flow_uo_evap_T_brine_min_jp,
                                tag_stc_flow_uo_evap_T_brine_max : stc_flow_uo_evap_T_brine_max_jp,
                                tag_stc_flow_uo_evap_press_spec_range : stc_flow_uo_evap_press_spec_range_jp,
                                tag_stc_flow_uo_evap_press_spec_min : stc_flow_uo_evap_press_spec_min_jp,
                                tag_stc_flow_uo_evap_press_spec_max : stc_flow_uo_evap_press_spec_max_jp,
                                tag_stc_flow_uo_evap_press_guide_range : stc_flow_uo_evap_press_guide_range_jp,
                                tag_stc_flow_uo_evap_press_guide_singlepoint : stc_flow_uo_evap_press_guide_singlepoint_jp,
                                tag_stc_flow_uo_evap_press_guide_min : stc_flow_uo_evap_press_guide_min_jp,
                                tag_stc_flow_uo_evap_press_guide_max : stc_flow_uo_evap_press_guide_max_jp,
                                tag_stc_flow_uo_evap_agitation_spec : stc_flow_uo_evap_agitation_spec_jp,
                                tag_stc_flow_uo_evap_agitation_arbitrary_with_guide : stc_flow_uo_evap_agitation_arbitrary_with_guide_jp,
                                tag_stc_flow_uo_evap_endpoint_spec_range : stc_flow_uo_evap_endpoint_spec_range_jp,
                                tag_stc_flow_uo_evap_endpoint_spec_min : stc_flow_uo_evap_endpoint_spec_min_jp,
                                tag_stc_flow_uo_evap_endpoint_spec_max : stc_flow_uo_evap_endpoint_spec_max_jp,
                                tag_stc_flow_uo_evap_endpoint_guide_range : stc_flow_uo_evap_endpoint_guide_range_jp,
                                tag_stc_flow_uo_evap_endpoint_guide_single : stc_flow_uo_evap_endpoint_guide_single_jp,
                                tag_stc_flow_uo_evap_endpoint_guide_min : stc_flow_uo_evap_endpoint_guide_min_jp,
                                tag_stc_flow_uo_evap_endpoint_guide_max : stc_flow_uo_evap_endpoint_guide_max_jp,
                                tag_stc_flow_uo_evap_rec_press : stc_flow_uo_evap_rec_vacuum_jp}
"""Japanese language dictionary for sentences for the unit operation evaporation"""

###################################################
#        PARTS FOR <unit operation>               #
###################################################

        #>>>>>>>>>>>>>> flowsheet compoentns in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<

#sets of:
#tag_part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr> = str
#part_flow_<unit operation>_<sort: instr, rec, mthod, etc>_<descr>_<lang> = str
#Follwed by 
#dict_<lang>_part_flow_<unit operation> = {<tag> : <component loc. lang>}


        #>>>>>>>>>>>>>> Template sentences for flow sheets in local language and tags (keys) thereof <<<<<<<<<<<<<<<<<<<
#tag_stc_<unit operation>_<item> = tag
#stc_stc_<unit operation>_<item>_<lang> = <str with placeholder>
#dict_<lang>_stcs_<unit operation> = {tag : sentence}
"""Language dictionary for instruction SENTENCES with place holders 'min' and/or 'max'. Use str.format()"""



############################################################################################################################################
#                                                       STYLE FOR OPEN PYXL                                                                #
############################################################################################################################################

#OpenPyXL styles
xl_line_thin = Side(style="thin")

xl_border_left = Border(left=xl_line_thin)
xl_border_right = Border(right=xl_line_thin)
xl_border_top = Border(top=xl_line_thin)
xl_border_bottom = Border(bottom=xl_line_thin)
xl_border_around = Border(left=xl_line_thin, right=xl_line_thin, top=xl_line_thin, bottom=xl_line_thin)

xl_alignment_center = Alignment(horizontal='center')
xl_alignment_left = Alignment(horizontal='left')

xl_font_bold = Font(bold=True)




