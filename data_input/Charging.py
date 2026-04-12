
import flow_draw.definitions as defs
from flow_draw.data_input import UnitOperation as uo
from typing import List

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
    
    def __init__(self, operation_seq=-1):
        self.unit_operation = uo.op_charging
        self.operation_seq = operation_seq
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
        print("Unit operation-"+str(self.operation_seq)+": Charging")
        print("How many input materials?: ", end="")
        self.material_count=int(input())
        for i in range(self.material_count):
            this_material = self.Material()
            this_material.test_data_creation()
            self.materials.append(this_material)
        print("test data created with "+str(self.material_count)+" material(s)")

    def output_unit_operation(self):
        self.flow_sheet.header_organizer(op_nr=self.operation_seq, title=self.unit_operation)
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flow_sheet.body_organizer(list_col_time=[],
                                           list_col_method=[],
                                           list_col_content=self.pre_comment,
                                           list_col_record=[],
                                           list_col_operator=[],
                                           list_col_witness=[])
        for material in self.materials:
            list_col_time=[]
            list_col_method=[]
            list_col_content=[]
            list_col_record=[]
            list_col_operator=[]
            list_col_witness=[]

            #line-1
            list_col_time.append(defs.part_time)
            list_col_method.append(material.method)
            list_col_content.append(material.name)
            list_col_record.append(defs.part_record_input)
            list_col_operator.append(defs.part_signature)
            list_col_witness.append(defs.part_signature)

            #line-2
            str_qty = str(material.qty_kg)+'±'+str(material.error_kg)+' kg'
            list_col_time
list_col_method
list_col_content
list_col_record
list_col_operator
list_col_witness



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
                self.qty_kg = self.chem_data.to_kilogram(material = self.name, equiv=self.metrics_val)
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
                for idx in range(len(Charging.list_charging_method)):
                    print(str(idx)+': '+Charging.list_charging_method[idx])
                print("> ", end='')
                choice_chargingmethod = int(input())
                self.method = Charging.list_charging_method[choice_chargingmethod]
            
            print("Specicfy a time control method?: ")
            for idx in range(len(Charging.list_time_control)):
                print(str(idx)+': '+Charging.list_time_control[idx])
            print("> ", end='')
            choice_time_control = int(input())
            self.time_control = Charging.list_time_control[choice_time_control]
            if self.time_control == Charging.time_control_min or self.time_control == Charging.time_control_min_max:
                print("Charging time lower limit?: ", end='')
                self.time_min = input()
            if self.time_control == Charging.time_control_max or self.time_control == Charging.time_control_min_max:
                print("Charging time upper limit?: ", end='')
                self.time_max = input()
            
            print("Specicfy a temperature control method?: ")
            for idx in range(len(Charging.list_temp_control)):
                print(str(idx)+': '+Charging.list_temp_control[idx])
            print("> ", end='')
            choice_temp_control = int(input())
            self.temp_control = Charging.list_temp_control[choice_temp_control]
            if self.temp_control == Charging.temp_control_min or self.temp_control == Charging.temp_control_min_max:
                print("Charging temperature (℃) lower limit?: ", end='')
                self.t_i_min = float(input())
            if self.temp_control == Charging.temp_control_max or self.temp_control == Charging.temp_control_min_max:
                print("Charging temperature (℃) upper limit?: ", end='')
                self.t_i_max = float(input())
            
            self.calc_qty()


        def test_data_creation(self):
            self.name = 'H2O'
            self.metrics_unit = defs.tag_metrics_vol
            self.metrics_val = 1.0
            self.error_pct = 5.0
            #self.qty_kg = None
            #self.error_kg = None
            self.method = Charging.charging_method_liq
            self.time_control = Charging.time_control_min
            self.time_min = '1h'
            self.time_max = None
            self.temp_control = Charging.temp_control_min_max
            self.t_i_min = 15
            self.t_i_max = 25
            self.calc_qty()




#charge = Charging(operation_seq=1)