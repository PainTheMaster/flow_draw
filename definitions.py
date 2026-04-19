import openpyxl as xl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment

#general
tag_yes = 'Yes'
tag_no = 'No'
list_yesno=[tag_no, tag_yes]

#Chemistry
tag_metrics_equiv = "equiv"
tag_metrics_vol = "v/w"

part_time = '___:___'
part_record_input = '仕込み量__________kg'
part_record_lot = 'ロット番号__________'
part_record_flex ='溶媒用フレキID__________'
part_record_temp_ini = '開始時内温_______℃'
part_record_temp_max = '仕込み時最大内温_______℃'
part_record_temp_min = '仕込み時最低内温_______℃'
part_record_temp_end = '終了時内温_______℃'
part_check_charged ='□ 仕込み実施'
part_signature = '   /  /  _____'


#OpenPyXL styles
xl_line_thin = Side(style="thin")

xl_line_left = Border(left=xl_line_thin)
xl_line_right = Border(right=xl_line_thin)
xl_line_top = Border(top=xl_line_thin)
xl_line_bottom = Border(bottom=xl_line_thin)
xl_line_around = Border(left=xl_line_thin, right=xl_line_thin, top=xl_line_thin, bottom=xl_line_thin)
xl_alignment_center = Alignment(horizontal='center')
xl_alignment_left = Alignment(horizontal='left')





