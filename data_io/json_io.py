from abc import ABC, abstractmethod
from typing import Literal
import json

class JsonEntity(ABC):
    def __init__(self,
                 key:str=None,
                 description:str=None,
                 required:bool=True):
        self.key=key
        self.description=description
        self.required=required

    @abstractmethod
    def asType(self)->list[str]:
        pass

    @abstractmethod
    def asEntity(self)->list[str]:
        pass

    def json_literal(self, value: str|int|float|bool) -> str:
        return json.dumps(value, ensure_ascii=False)

class Array(JsonEntity):
    def __init__(self,
                key:str=None,
                content:JsonEntity | list[JsonEntity]=None,
                description:str=None,
                required:bool=True):
        super().__init__(key=key, description=description, required=required)
        self.content=content
        if key is None:
            raise ValueError(f'{self.__class__.__name__}: "key" not given.')        
        if content is None:
            raise ValueError(f'{self.__class__.__name__}: "content" not given.')
        if isinstance(self.content, list) and len(self.content) == 0:
            raise ValueError(f'{self.__class__.__name__}: An empty list is put in "content".')
    
    def asType(self)->list[str]:
        list_json_str:list[str] = []
        list_json_str.append('{')
        if self.description is not None:
            list_json_str.append(f' "description":{self.json_literal(self.description)},')
        list_json_str.append(' "type":"array",')

        if isinstance(self.content, JsonEntity):
            lines:list[str] = self.content.asType()
            lines[0] = '"items":'+lines[0]
            for single_line in lines:
                list_json_str.append(' '+single_line)
        elif isinstance(self.content, list) and isinstance(self.content[0], JsonEntity):
            list_json_str.append(' "items":{')
            list_json_str.append('  "oneOf":[')
            for entity in self.content:
                for single_line in entity.asType():
                    list_json_str.append('   '+single_line)
                list_json_str[-1] +=','
            list_json_str[-1]=list_json_str[-1].removesuffix(',')
            list_json_str.append('  ]')
            list_json_str.append(' }')
        else:
            raise TypeError(f'{self.__class__.__name__}: invalid "content" type')

        list_json_str.append('}')
        return list_json_str
    
    def asEntity(self)->list[str]:
        list_json_str:list[str] = self.asType()
        list_json_str[0] =f'{self.json_literal(self.key)}:'+list_json_str[0]
        return list_json_str

            
class Objason(JsonEntity):
    def __init__(self,
                key:str=None,
                props: list[JsonEntity]=None,
                description:str=None,
                required:bool=True):
        super().__init__(key=key, description=description, required=required)
        if key is None:
            raise ValueError(f'{self.__class__.__name__}: "key" not given.')  
        self.props=props
        if props is None or len(props)==0:
            raise ValueError(f'{self.__class__.__name__}: Property not given.')
    
    def asType(self)->list[str]:
        list_json_str: list[str] = []
        list_json_str.append('{')
        if self.description is not None:
            list_json_str.append(f' "description":{self.json_literal(self.description)},')
        list_json_str.append(' "type":"object",')
        list_json_str.append(' "properties":{')
        required:str=''
        for single_prop in self.props:
            for line in single_prop.asEntity():
                list_json_str.append('  '+line)
            list_json_str[-1] += ','
            if single_prop.required:
                required += f'{self.json_literal(single_prop.key)},'
        list_json_str[-1]=list_json_str[-1].removesuffix(',')
        list_json_str.append(' }')

        required=required.removesuffix(',')
        if required != '':
            list_json_str[-1]+=','
            list_json_str.append(f' "required":[{required}]')
        
        list_json_str.append('}')

        return list_json_str

    def asEntity(self)->list[str]:
        list_json_str:list[str] = self.asType()
        list_json_str[0] =f'{self.json_literal(self.key)}:'+list_json_str[0]
        return list_json_str

        
class Primitive(JsonEntity):
    def __init__(self,
                 prim_type:Literal['string','integer', 'number','boolean'] = None,
                 key:str = None,
                 description:str = None,
                 enum:list[str]|list[int]|list[float]|list[bool] = None,
                 const:str|int|float|bool = None,
                 required:bool = True):
        super().__init__(key=key, description=description, required=required)
        self.prim_type:str = prim_type
        self.enum:list[str]|list[int]|list[float]|list[bool] = enum
        self.const:str|int|float|bool = const
        if key is None:
            raise ValueError(f'{self.__class__.__name__}: "key" not given.')  
        if enum is not None and const is not None:
            raise ValueError(f'{self.__class__.__name__}: "enum" and "const" are given at the same time.')
        if prim_type is None:
            raise ValueError(f'{self.__class__.__name__}: Type not selected.')
        # if const is True:
        #     const = 'true'
        # elif const is False:
        #     const = 'false'

    
    def asType(self)->list[str]:
        list_json_str: list[str] = []
        list_json_str.append('{')
        if self.description is not None:
            list_json_str.append(f' "description":{self.json_literal(self.description)},')
        list_json_str.append(f' "type":"{self.prim_type}",')

        if self.enum is not None:
            enum_values = ','.join(self.json_literal(item) for item in self.enum)
            list_json_str.append(f' "enum":[{enum_values}],')

        if self.const is not None:
            list_json_str.append(f' "const":{self.json_literal(self.const)},')

        list_json_str[-1]=list_json_str[-1].removesuffix(',')
        list_json_str.append('}')
        return list_json_str
    

    def asEntity(self)->list[str]:
        list_json_str:list[str] = self.asType()
        list_json_str[0] =f'{self.json_literal(self.key)}:'+list_json_str[0]
        return list_json_str
    
            
