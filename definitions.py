import openpyxl as xl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment
from openpyxl.styles import Font

###############################################
#ITEMS FOR INTERNAL DATA PROCESSING: TAGS ETC #
###############################################

#general
tag_yes = 'Yes'
tag_no = 'No'
list_yesno=[tag_no, tag_yes]




################################################################
#PARTS FOR PROCESS DATA IO: HEADER ITEMS, DROP-DOWN OPTIONS ETC#
################################################################

####CHARGING####
tag_metrics_equiv = "equiv"
tag_metrics_vol = "v/w"
list_metrics_unit = [tag_metrics_equiv, tag_metrics_vol]
"""For process.unit_operations.charging.Charging. This is for drop-down list in the detail input form."""




################################################################
#                      PARTS FLOW SHEETS                       #
################################################################

#####COMMON####
part_time = '___:___' 
"""Common flowsheet component to record a point of time some action is taken."""
part_signature = '   /  /  _____'
"""Common flowsheet component for a signature"""



####CHARGING####
part_method_charging_ini = '仕込み開始'
"""Flowseet component for class Charging. An action item of commencement of charging/dosing"""

part_method_charging_end = '仕込み終了'
"""Flowseet component for class Charging. An action item of end of charging/dosing"""

part_record_input = '仕込み量__________kg'
"""Flowseet component for class Charging. A recording element for dispensed amount"""

part_record_lot = 'ロット番号__________'
"""Flowseet component for class Charging. A recording element for the lot number of a material"""

part_record_flex ='溶媒用フレキID__________'
"""Flowseet component for class Charging. A recording element for the ID of flexible tube for solvents"""

part_record_temp_ini = '開始時内温_______℃'
"""Flowseet component for class Charging. A recording element for initial temperature of a certain action"""

part_record_temp_max = '仕込み時最高内温_______℃'
"""Flowseet component for class Charging. A recording element for the maximum temperature"""

part_record_temp_min = '仕込み時最低内温_______℃'
"""Flowseet component for class Charging. A recording element for the minimum"""

part_record_temp_end = '終了時内温_______℃'
"""Flowseet component for class Charging. A recording element for the terminal temperature"""

part_check_charged ='□ 仕込み実施'
"""Flowseet component for class Charging. A check box for complete charging/dosing"""



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




