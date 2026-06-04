

# class JSON_property:
#     def __init__(self):
#         self.list_property: list[SingleProperty] = []
    
#     def add(self,
#             property_name:str =None,
#             data_type:str = None,
#             enum_opt:list[any] = None,
#             arr_obj : JSON_property = None,
#             description:str = None,
#             required:bool = None,
#             ):
#         new_entry = SingleProperty(property_name=property_name,
#                                     data_type=data_type,
#                                     enum_opt=enum_opt,
#                                     description=description,
#                                     required=required,
#                                     sub_object=sub_object)
#         self.list_property.append(new_entry)
    
#     def toJSON(self):
#         json: list[str] = ""
        
        
        

# class SingleProperty:
#     def __init__(self,
#             property_name:str =None,
#             data_type:str = None,
#             enum_opt:list[any] = [],
#             arr_obj : JSON_property = None,
#             description:str = None,
#             required:bool = None,
#             ):
#         self.property_name:str = property_name
#         self.type:str = data_type
#         self.enum_opt: list[any] = enum_opt
#         self.description:str = description
#         self.required:bool = required

#     def toJSON(self)->list[str]:
#         json: list[str] = []
#         json.append(f'"{self.property_name}":{{')
#         if self.description is not None:
#             json.append(f'\t"description":"{self.description}",')
#         json.append(f'\t"type":"{self.type}",')
#         if len(self.enum_opt) > 0:
#             temp_array:str = '"['
#             i: int = 0
#             for i in range(len(self.enum_opt)-1):
#                 temp_array+='"'+self.enum_opt[i]+'"'+','
#             temp_array+='"'+self.enum_opt[i]+'"'+']'
#             json.append(f'\t"enum":{temp_array},')
#         json[-1]=json[-1].removesuffix(',')
#         json.append('}')
#         return json


class JSONentry:
    def __init__(self,
            property_name:str =None,
            data_type:str = None,
            enum_opt:list[any] = None,
            arr_obj : list[JSONentry] = None,
            description:str = None,
            required:bool = None,
            ):
        self.property_name:str = property_name
        self.data_type:str = data_type
        self.enum_opt: list[any] = enum_opt
        self.arr_obj : list[JSONentry] = arr_obj,
        self.description:str = description
        self.required:bool = required

    def nest(self, entry):
        pass

    def toJSON(self)->list[str]:
        json: list[str] = []
        json.append(f'"{self.property_name}":{{')
        if self.description is not None:
            json.append(f' "description":"{self.description}",')
        json.append(f' "type":"{self.data_type}",')
        if self.enum_opt is not None:
            temp_array:str = '['
            i: int = 0
            for i in range(len(self.enum_opt)-1):
                temp_array+=f'"{self.enum_opt[i]}",'
            temp_array+=f'"{self.enum_opt[i]}"]'
            json.append(f' "enum":{temp_array},')
        if self.data_type=="array" and self.arr_obj is not None:
            json.append(' "items:{"')
            inner_obj_lines = self.arr_obj.toJSON
            for line in inner_obj_lines:
                json.append('  '+line)
            json.append(' }')
        if self.data_type=="object":
            json.append('"properties:{"')
            for prop in self.arr_obj:
                json_prop=prop.toJSON()
                for line in json_prop:
                    json.append(f' {line}')
                json[-1]+=','
            json[-1]=json[-1].removesuffix(',')
            json.append('},')
            required:str='"required":['
            for prop in self.arr_obj:
                if prop.required:
                    required += f'"{prop.property_name}",'
            required=required.removesuffix(',')
            required+='],'
            json.append(required)
            json.append('""additionalProperties": false"')

            
        json[-1]=json[-1].removesuffix(',')
        json.append('}')
        return json
        

    


