
import flow_draw.definitions as defs
from flow_draw.data_input import UnitOperation as uo
from typing import List


charging_method_liq = 'liquid_port'
charging_method_shower = 'shower'
charging_method_press = 'press_vessel'
charging_method_pow ='powder_port'
charging_method_placeholder = 'placeholder'
list_charging_method =[charging_method_liq,
                    charging_method_shower,
                    charging_method_press,
                    charging_method_pow,
                    charging_method_placeholder
                    ]

time_control_none = "No time control"
time_control_min="Time control with minimum"
time_control_max="Time control with maximum"
time_control_min_max='Time control with minimum and maximum'
time_control_placeholder = 'Placeholder'
list_time_control =[
    time_control_none,
    time_control_min,
    time_control_max,
    time_control_min_max,
    time_control_placeholder
]

temp_control_none = "No temp control"
temp_control_min="Temp control with minimum"
temp_control_max="Temp control with maximum"
temp_control_min_max='Temp control with minimum and maximum'
temp_control_placeholder = 'Placeholder'
list_temp_control =[
    temp_control_none,
    temp_control_min,
    temp_control_max,
    temp_control_min_max,
    temp_control_placeholder
]


class Charging(uo.UnitOperation):
    """
    Inherited:
        self.unit_operation: str
        self.operation_seq: int
        self.pre_comment: str
        self.post_commnt: str
    
    New here:
        self.material_count
        self.materials[]

    """
    list_metrics_unit = [defs.tag_metrics_equiv, defs.tag_metrics_vol]

    #dict_error_range={1:1.0, 5:5.0, 6:"place holder"}
    error_range_placeholder='place holder'
    list_error_range = [None, 1.0, None, None, None, 5.0, error_range_placeholder]


    
    def __init__(self, operation_seq=None):
        super().__init__(unit_operation=uo.op_charging, operation_seq=operation_seq)
        self.material_count = 0
        self.materials: List[Charging.Material] = []


    def interact(self):
        print("Unit operation-"+str(self.operation_seq)+": Charging")
        print("Pre-comment?:")
        self.pre_comment = input()
        print("How many input materials?: ", end="")
        self.material_count=int(input())
        for i in range(self.material_count):
            this_material = self.Material()
            this_material.interact()
            self.materials.append(this_material)
        print("Post-comment?:")
        self.post_comment = input()

    def test_data_creation(self):
        # print("Unit operation-"+str(self.operation_seq)+": Charging")
        # print("How many input materials?: ", end="")
        # self.material_count=int(input())
        # for i in range(self.material_count):
        #     this_material = self.Material()
        #     this_material.test_data_creation()
        #     self.materials.append(this_material)
        # print("test data created with "+str(self.material_count)+" material(s)")

        self.pre_comment = 'This is the line-1 of a dummy pre-comment\nThis is the line-2 of a dummy pre-comment'
        self.post_comment = 'This is the line-1 of a dummy post-comment;This is the line-2 of a dummy post-comment;The product is salty.'
        material_count = 2
        material1 = self.Material()
        material1.test_data_creation1()
        self.materials.append(material1)
        material2 = self.Material()
        material2.test_data_creation2()
        self.materials.append(material2)
        print("Test data created for salt water.")

    def output_unit_operation(self):
        self.flow_sheet.header_organizer(op_nr=self.operation_seq, title=self.unit_operation)
        list_col_time: List[str] = []
        list_col_method: List[str]=[]
        list_col_content: List[str]=[]
        list_col_record: List[str]=[]
        list_col_operator: List[str]=[]
        list_col_witness: List[str]=[]
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.put_comment(comments=self.pre_comment,
                            list_col_time=list_col_time,
                            list_col_method=list_col_method,
                            list_col_content=list_col_content,
                            list_col_record=list_col_record,
                            list_col_operator=list_col_operator,
                            list_col_witness=list_col_witness)
            self.flow_sheet.body_organizer(list_col_time=list_col_time,
                                           list_col_method=list_col_method,
                                           list_col_content=list_col_content,
                                           list_col_record=list_col_record,
                                           list_col_operator=list_col_operator,
                                           list_col_witness=list_col_witness)

        for material in self.materials:
            list_col_time.clear()
            list_col_method.clear()
            list_col_content.clear()
            list_col_record.clear()
            list_col_operator.clear()
            list_col_witness.clear()

            #line-1: RM name, charging method, lot record
            list_col_time.append(defs.part_time)
            list_col_method.append(material.method)
            list_col_content.append(material.name)
            list_col_record.append(defs.part_record_lot)
            list_col_operator.append(defs.part_signature)
            list_col_witness.append(defs.part_signature)

            #line-2: QTY instruction and record
            str_qty = str(material.qty_kg)+'±'+str(material.error_kg)+' kg'
            list_col_time.append(None)
            list_col_method.append(None)
            list_col_content.append(str_qty)
            list_col_record.append(defs.part_record_input)
            list_col_operator.append(None)
            list_col_witness.append(None)
            
            self.flow_sheet.body_organizer(list_col_time=list_col_time,
                                           list_col_method=list_col_method,
                                           list_col_content=list_col_content,
                                           list_col_record=list_col_record,
                                           list_col_operator=list_col_operator,
                                           list_col_witness=list_col_witness)

            #For liquid only, flex ID 
            if (material.method == charging_method_liq or
                material.method == charging_method_press or
                material.method == charging_method_shower):

                list_col_time.append(None)
                list_col_method.append(None)
                list_col_content.append(None)
                list_col_record.append(defs.part_record_flex)
                list_col_operator.append(defs.part_signature)
                list_col_witness.append(defs.part_signature)

                self.flow_sheet.body_organizer(list_col_time=list_col_time,
                                           list_col_method=list_col_method,
                                           list_col_content=list_col_content,
                                           list_col_record=list_col_record,
                                           list_col_operator=list_col_operator,
                                           list_col_witness=list_col_witness)
            
            #for both liq and solid; temp and time control.
            if not (material.time_control == time_control_none or material.time_control is None):
                self.put_time_control(material=material,
                                        col_time=list_col_time,
                                        col_method=list_col_method,
                                        col_content=list_col_content,
                                        col_record=list_col_record,
                                        col_operator=list_col_operator,
                                        col_witness=list_col_witness)
                self.flow_sheet.body_organizer(list_col_time=list_col_time,
                                           list_col_method=list_col_method,
                                           list_col_content=list_col_content,
                                           list_col_record=list_col_record,
                                           list_col_operator=list_col_operator,
                                           list_col_witness=list_col_witness)

            if not (material.temp_control == temp_control_none or material.temp_control is None):
                self.put_temp_control(material=material,
                                        col_time=list_col_time,
                                        col_method=list_col_method,
                                        col_content=list_col_content,
                                        col_record=list_col_record,
                                        col_operator=list_col_operator,
                                        col_witness=list_col_witness)              
                self.flow_sheet.body_organizer(list_col_time=list_col_time,
                                           list_col_method=list_col_method,
                                           list_col_content=list_col_content,
                                           list_col_record=list_col_record,
                                           list_col_operator=list_col_operator,
                                           list_col_witness=list_col_witness)

            self.put_end_of_dosing(col_time=list_col_time,
                                    col_method=list_col_method,
                                    col_content=list_col_content,
                                    col_record=list_col_record,
                                    col_operator=list_col_operator,
                                    col_witness=list_col_witness)
            self.flow_sheet.body_organizer(list_col_time=list_col_time,
                                        list_col_method=list_col_method,
                                        list_col_content=list_col_content,
                                        list_col_record=list_col_record,
                                        list_col_operator=list_col_operator,
                                        list_col_witness=list_col_witness)
            self.flow_sheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.put_comment(comments=self.post_comment,
                            list_col_time=list_col_time,
                            list_col_method=list_col_method,
                            list_col_content=list_col_content,
                            list_col_record=list_col_record,
                            list_col_operator=list_col_operator,
                            list_col_witness=list_col_witness)
            self.flow_sheet.body_organizer(list_col_time=list_col_time,
                                            list_col_method=list_col_method,
                                            list_col_content=list_col_content,
                                            list_col_record=list_col_record,
                                            list_col_operator=list_col_operator,
                                            list_col_witness=list_col_witness)
            self.flow_sheet.linefeed()
            


    def put_time_control(self, material: Charging.Material,
                         col_time: List[str],
                         col_method: List[str],
                         col_content: List[str],
                         col_record: List[str],
                         col_operator: List[str],
                         col_witness: List[str]):

        if (material.time_control == time_control_min):
            sentece_instruction = "*滴下時間"+str(material.time_min)+"以上"
            col_time.append(defs.part_time)
            col_method.append("仕込み開始")
            col_content.append(sentece_instruction)
            col_record.append(None)
            col_operator.append(defs.part_signature)
            col_witness.append(defs.part_signature)

        elif (material.time_control == time_control_max):
            sentece_instruction = "*滴下時間"+str(material.time_max)+"以内"
            col_time.append(defs.part_time)
            col_method.append("仕込み開始")
            col_content.append(sentece_instruction)
            col_record.append(None)
            col_operator.append(defs.part_signature)
            col_witness.append(defs.part_signature)    

        elif (material.time_control == time_control_min_max):
            sentece_instruction = "*滴下時間"+str(material.time_min)+"～"+str(material.time_max)+"以内"
            col_time.append(defs.part_time)
            col_method.append("仕込み開始")
            col_content.append(sentece_instruction)
            col_record.append(None)
            col_operator.append(defs.part_signature)
            col_witness.append(defs.part_signature)


    def put_temp_control(self, material: Charging.Material,
                         col_time: List[str],
                         col_method: List[str],
                         col_content: List[str],
                         col_record: List[str],
                         col_operator: List[str],
                         col_witness: List[str]):
        if material.temp_control == temp_control_min:
            sentence = "仕込み時内温"+str(material.t_i_min)+"℃以上"
            col_time.append(None)
            col_method.append(None)
            col_content.append(sentence)
            col_record.append(defs.part_record_temp_ini)
            col_operator.append(None)
            col_witness.append(None)

            col_time.append(None)
            col_method.append(None)
            col_content.append(None)
            col_record.append(defs.part_record_temp_min)
            col_operator.append(None)
            col_witness.append(None)

            col_time.append(None)
            col_method.append(None)
            col_content.append(None)
            col_record.append(defs.part_record_temp_max)
            col_operator.append(None)
            col_witness.append(None)

            col_time.append(None)
            col_method.append(None)
            col_content.append(None)
            col_record.append(defs.part_record_temp_end)
            col_operator.append(None)
            col_witness.append(None)
        elif material.temp_control == temp_control_max:
            sentence = "仕込み時内温"+str(material.t_i_max)+"℃以下"
            sentence = "仕込み時内温"+str(material.t_i_min)+'～'+str(material.t_i_max)+"℃"
            col_time.append(None)
            col_method.append(None)
            col_content.append(sentence)
            col_record.append(defs.part_record_temp_ini)
            col_operator.append(None)
            col_witness.append(None)

            col_time.append(None)
            col_method.append(None)
            col_content.append(None)
            col_record.append(defs.part_record_temp_max)
            col_operator.append(None)
            col_witness.append(None)

            col_time.append(None)
            col_method.append(None)
            col_content.append(None)
            col_record.append(defs.part_record_temp_end)
            col_operator.append(None)
            col_witness.append(None)

        elif material.temp_control == temp_control_min_max:
            sentence = "仕込み時内温"+str(material.t_i_min)+'～'+str(material.t_i_max)+"℃"
            col_time.append(None)
            col_method.append(None)
            col_content.append(sentence)
            col_record.append(defs.part_record_temp_ini)
            col_operator.append(None)
            col_witness.append(None)

            col_time.append(None)
            col_method.append(None)
            col_content.append(None)
            col_record.append(defs.part_record_temp_min)
            col_operator.append(None)
            col_witness.append(None)

            col_time.append(None)
            col_method.append(None)
            col_content.append(None)
            col_record.append(defs.part_record_temp_max)
            col_operator.append(None)
            col_witness.append(None)

            col_time.append(None)
            col_method.append(None)
            col_content.append(None)
            col_record.append(defs.part_record_temp_end)
            col_operator.append(None)
            col_witness.append(None)

    def put_end_of_dosing(self,
                         col_time: List[str],
                         col_method: List[str],
                         col_content: List[str],
                         col_record: List[str],
                         col_operator: List[str],
                         col_witness: List[str]):

            col_time.append(defs.part_time)
            col_method.append("仕込み終了")
            col_content.append(None)
            col_record.append(defs.part_check_charged)
            col_operator.append(defs.part_signature)
            col_witness.append(defs.part_signature)



    class Material:
        """This class is for each material charged, each instance correspnds to each dosage in a charging operation.
        """
        def __init__(self):
            self.name = ""
            self.metrics_unit = ""
            self.metrics_val = None
            self.error_pct = None
            self.qty_kg = None
            self.error_kg = None
            self.method = ""
            self.time_control = None
            self.time_min = None
            self.time_max = None
            self.temp_control = None
            self.t_i_min = None
            self.t_i_max = None

        def calc_qty(self):
            """Calculates the quantity of the material and permissible error in "kg" unit. 
            """
            if self.metrics_unit == defs.tag_metrics_equiv:
                self.qty_kg = uo.UnitOperation.chem_data.to_kilogram(material = self.name, equiv=self.metrics_val)
                self.error_kg = self.qty_kg * (self.error_pct/100.0)
            elif self.metrics_unit == defs.tag_metrics_vol:
                self.qty_kg = uo.UnitOperation.chem_data.to_kilogram(material = self.name, vol=self.metrics_val)
                self.error_kg = self.qty_kg * (self.error_pct/100.0)
            else:
                raise ValueError('metrics_unit not defined')
        
        def interact(self):
            print("Material name?: ", end='')
            self.name = input()
        
            print("Metrics unit?: ")
            for idx in range(len(Charging.list_metrics_unit)):
                print(str(idx)+": "+Charging.list_metrics_unit[idx])
            print("> ", end='')
            idx = int(input())
            self.metrics_unit = Charging.list_metrics_unit[idx]
            
            print("Metrics value?: ", end='')
            self.metrics_val = float(input())

            
            print('Permissible error?:')
            for idx in range(len(Charging.list_error_range)):
                if Charging.list_error_range[idx] is not None:
                    print(str(idx)+": "+str(Charging.list_error_range[idx])+"%")
            print("> ", end='')
            choice_error_range = int(input())
            self.error_pct = Charging.list_error_range[choice_error_range]

            print('Specify a charging method?:')
            for idx in range(len(defs.list_yesno)):
                print(str(idx)+': '+defs.list_yesno[idx])
            print("> ", end='')
            specif_yesno = int(input())
            if defs.list_yesno[specif_yesno] == defs.tag_yes:
                for idx in range(len(list_charging_method)):
                    print(str(idx)+': '+list_charging_method[idx])
                print("> ", end='')
                choice_chargingmethod = int(input())
                self.method = list_charging_method[choice_chargingmethod]
            
            print("Specicfy a time control method?: ")
            for idx in range(len(list_time_control)):
                print(str(idx)+': '+list_time_control[idx])
            print("> ", end='')
            choice_time_control = int(input())
            self.time_control = list_time_control[choice_time_control]
            if self.time_control == time_control_min or self.time_control == time_control_min_max:
                print("Charging time lower limit?: ", end='')
                self.time_min = input()
            if self.time_control == time_control_max or self.time_control == time_control_min_max:
                print("Charging time upper limit?: ", end='')
                self.time_max = input()
            
            print("Specicfy a temperature control method?: ")
            for idx in range(len(list_temp_control)):
                print(str(idx)+': '+list_temp_control[idx])
            print("> ", end='')
            choice_temp_control = int(input())
            self.temp_control = list_temp_control[choice_temp_control]
            if self.temp_control == temp_control_min or self.temp_control == temp_control_min_max:
                print("Charging temperature (℃) lower limit?: ", end='')
                self.t_i_min = float(input())
            if self.temp_control == temp_control_max or self.temp_control == temp_control_min_max:
                print("Charging temperature (℃) upper limit?: ", end='')
                self.t_i_max = float(input())
            
            self.calc_qty()


        def test_data_creation1(self):
            self.name = 'H2O'
            self.metrics_unit = defs.tag_metrics_vol
            self.metrics_val = 1.0
            self.error_pct = 5.0
            #self.qty_kg = None
            #self.error_kg = None
            self.method = charging_method_liq
            self.time_control = time_control_min
            self.time_min = '1h'
            self.time_max = None
            self.temp_control = temp_control_min_max
            self.t_i_min = 15
            self.t_i_max = 25
            self.calc_qty()

        def test_data_creation2(self):
            self.name = 'NaCl'
            self.metrics_unit = defs.tag_metrics_equiv
            self.metrics_val = 2.0
            self.error_pct = 5.0
            #self.qty_kg = None
            #self.error_kg = None
            self.method = charging_method_pow
            self.time_control = time_control_none
            self.time_min = None
            self.time_max = None
            self.temp_control = temp_control_min_max
            self.t_i_min = 15
            self.t_i_max = 25
            self.calc_qty()




#charge = Charging(operation_seq=1)