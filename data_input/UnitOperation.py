import json
from flow_draw import definitions as defs
from flow_draw import chemistry as chem


op_line_clearance = "line_clearance"
op_N2_replace = "N2_placement"
op_temp_control = "temp_control"
op_charging = "charging"
op_agitation = "agitation"
op_settling = "settling"
op_aq_discharge = "aq_discharge"
op_distillation = "distillation"
op_cip = "cip"
op_transfer = "transfer"
op_filtration = "filtration"
op_rinse = "rinse"
op_reslurry = "reslurry"
op_drying = "drying"
op_tare = "tare"
op_prod_discharge = "prod_discharge"
op_placeholder = "placeholder"


# list_metrics_unit = [defs.tag_metrics_equiv, defs.tag_metrics_vol]

# #dict_error_range={1:1.0, 5:5.0, 6:"place holder"}
# error_range_placeholder='place holder'
# list_error_range = [None, 1.0, None, None, None, 5.0, error_range_placeholder]

# charging_method_liq = 'liquid_port'
# charging_method_shower = 'shower'
# charging_method_press = 'press_vessel'
# charging_method_pow ='powder_port'
# charging_method_placeholder = 'placeholder'
# list_charging_method =[charging_method_liq,
#                        charging_method_shower,
#                        charging_method_press,
#                        charging_method_pow,
#                        charging_method_placeholder
#                        ]


class UnitOperation:
    chem_data = None
    def __init__(self, unit_operation="", operation_seq=-1):
        self.unit_operation = unit_operation
        self.operation_seq = operation_seq
        self.pre_comment = ''
        self.post_comment = ''
    @classmethod 
    def set_chemdata(cls, chem_data:chem.Chemistry):
        cls.chem_data = chem_data




# class Charging(UnitOperation):
#     """
#     Inherited:
#         self.unit_operation: str
#         self.operation_seq: int
#         self.pre_comment: str
#         self.post_commnt: str
    
#     New here:
#         self.material_count
#         self.materials[]

#     """
#     list_metrics_unit = [defs.tag_metrics_equiv, defs.tag_metrics_vol]

#     #dict_error_range={1:1.0, 5:5.0, 6:"place holder"}
#     error_range_placeholder='place holder'
#     list_error_range = [None, 1.0, None, None, None, 5.0, error_range_placeholder]

#     charging_method_liq = 'liquid_port'
#     charging_method_shower = 'shower'
#     charging_method_press = 'press_vessel'
#     charging_method_pow ='powder_port'
#     charging_method_placeholder = 'placeholder'
#     list_charging_method =[charging_method_liq,
#                         charging_method_shower,
#                         charging_method_press,
#                         charging_method_pow,
#                         charging_method_placeholder
#                         ]

#     time_control_none = "No time control"
#     time_control_min="Time control with minimum"
#     time_control_max="Time control with maximum"
#     time_control_min_max='Time control with minimum and maximum'
#     time_control_placeholder = 'Placeholder'
#     list_time_control =[
#         time_control_none,
#         time_control_min,
#         time_control_max,
#         time_control_min_max,
#         time_control_placeholder
#     ]
    
#     def __init__(self, operation_seq=-1):
#         self.unit_operation = op_charging
#         self.operation_seq = operation_seq
#         self.material_count = 0
#         self.materials = []
#         self.interact()

#     def interact(self):
#         print("Unit operation-"+str(self.operation_seq)+": Charging")
#         print("How many input materials?: ", end="")
#         self.material_count=int(input())
#         for i in range(self.material_count):
#             this_material = self.Material()
#             self.materials.append(this_material)


#     class Material():
#         """This class is for each material charged, each instance correspnds to each dosage in a charging operation.
#         """
#         def __init__(self):
#             self.name = ""
#             self.metrics_unit = ""
#             self.metrics_val = None
#             self.error_pct = None
#             self.qty_kg = None
#             self.error_kg = None
#             self.method = ""
#             self.time_control = None
#             self.time_min = None
#             self.time_max = None
#             self.temp_control = None
#             self.t_i_min = None
#             self.t_i_max = None
#             self.interact()
#             self.calc_qty()

#         def calc_qty(self):
#             """Calculates the quantity of the material and permissible error in "kg" unit. 
#             """
#             if self.metrics_unit == defs.tag_metrics_equiv:
#                 self.qty_kg = self.chem_data.to_kilogram(material = self.name, equiv=self.metrics_val)
#                 self.error_kg = self.qty_kg * (self.error_pct/100.0)
#             elif self.metrics_unit == defs.tag_metrics_vol:
#                 self.qty_kg = Charging.chem_data.to_kilogram(material = self.name, vol=self.metrics_val)
#                 self.error_kg = self.qty_kg * (self.error_pct/100.0)
#             else:
#                 raise ValueError('metrics_unit not defined')
        
# def interact(self):
#             print("Material name?: ", end='')
#             self.name = input()
           
#             print("Metrics unit?: ")
#             for idx in range(len(Charging.list_metrics_unit)):
#                 print(str(idx)+": "+Charging.list_metrics_unit[idx])
#             print("> ", end='')
#             idx = int(input())
#             self.metrics_unit = Charging.list_metrics_unit[idx]
            
#             print("Metrics value?: ", end='')
#             self.metrics_val = float(input())

            
#             print('permissible error?:')
#             for idx in range(len(Charging.list_error_range)):
#                 if Charging.list_error_range[idx] is not None:
#                     print(str(idx)+": "+str(Charging.list_error_range[idx])+"%")
#             print("> ", end='')
#             choice_error_range = int(input())
#             self.error_pct = Charging.list_error_range[choice_error_range]

#             print('Specify a charging method?:')
#             for idx in range(len(defs.list_yesno)):
#                 print(str(idx)+': '+defs.list_yesno[idx])
#             print("> ", end='')
#             specif_yesno = int(input())
#             if defs.list_yesno[specif_yesno] == defs.tag_yes:
#                 for idx in range(len(Charging.list_charging_method)):
#                     print(str(idx)+': '+Charging.list_charging_method[idx])
#                 print("> ", end='')
#                 choice_chargingmethod = int(input())
#                 self.method = Charging.list_charging_method[choice_chargingmethod]
            
#             print("Specicfy a time control method?: ", end='')
#             for idx in range(len(Charging.list_time_control)):
#                 print(str(idx)+': '+Charging.list_time_control[idx])
#             print("> ", end='')
#             choice_time_control = int(input())
#             self.time_control = Charging.list_time_control[choice_time_control]
#             if self.time_control == Charging.time_control_min or self.time_control == Charging.time_control_min_max:
#                 print("Chargint time lower limit?: ", end='')
#                 self.time_min = int(input())
#             if self.time_control == Charging.time_control_max or self.time_control == Charging.time_control_min_max:
#                 print("Chargint time upper limit?: ", end='')
#                 self.time_max = int(input())
            
#             print(str(self))
                        


            


    # print('Specify a something method?:')
    #     for idx in range(len(defs.list_yesno)):
    #         print(str(idx)+': '+defs.list_yesno[idx])
    #     print("> ", end='')

    # print("?: ", end='')
    # for idx in range(len(something)):
    #     print(str(idx)+': '+something[idx])
    # print("> ", end='')

    # print("?: ", end='')
    # something = int(input())
    # print("> ", end='')

    


        
