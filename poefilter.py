import copy
from textwrap import dedent, indent
from poepy_core import BaseTypeString

SHOW = 1
HIDE = 2
DISABLE = 3

def CustomSound(name, atype='mp3'):
    return f'"{name}.{atype}"'

class Style:
    def __init__(self, SetFontSize=45, SetTextColor=None, SetBackgroundColor=None, 
    SetBorderColor=None, MinimapIcon=None, PlayEffect=None, PlayAlertSound=None, CustomAlertSound=None):
        self.attributes = {}
        self.attributes['SetFontSize'] = SetFontSize
        self.attributes['SetTextColor'] = SetTextColor
        self.attributes['SetBackgroundColor'] = SetBackgroundColor
        self.attributes['SetBorderColor'] = SetBorderColor
        self.attributes['MinimapIcon'] = MinimapIcon
        self.attributes['PlayEffect'] = PlayEffect
        self.attributes['PlayAlertSound'] = PlayAlertSound
        self.attributes['CustomAlertSound'] = CustomAlertSound

    def __str__(self):
        ret = ""
        for att, val in self.attributes.items():
            ret += f'{att} {val}\n' if val is not None else ""
        return ret.strip()

    def __repr__(self):
        return self.__str__()

    def changed_copy(self, **kwargs):
        ret = copy.deepcopy(self)
        for k, v in kwargs.items():
            ret.attributes[k] = v
        return ret

class FilterObj:
    def __init__(self, comment="Filter header comment"):
        self.comment = comment
        self.sections = {}

    def append(self, section):
        self.sections[section.comment] = section

    def exception_from_section(self, section_name):
        return [cat for cat in self.sections[section_name].categories.values() if 'Exception' in cat.comment]

    def __str__(self):
        ret = f'# {self.comment}\n'
        for section in self.sections.values():
            ret += f'{section}'
        return ret

    def __repr__(self):
        return self.__str__()

class Section:

    def __init__(self, comment="UNTITLED SECTION", *initial_categories):
        self.comment = comment
        self.categories = {}
        for category in initial_categories:
            self.append(category)

    def append(self, category):
        self.categories[category.comment] = category

    def __str__(self):
        ret = ''
        ret += f'#{"---"*36}\n'
        ret += f'# Section:\t#\t{self.comment}\n'
        ret += f'#{"---"*36}\n'
        for category in self.categories.values():
            if category.show != DISABLE:
                ret += indent(f'{category}', '\t')
        return ret

    def __repr__(self):
        return self.__str__()

class Category:
    # def __init__(self, comment="Untitled Category", show=True, classes=None, base_type=None, rarity=None, sockets=None, linked_sockets=None, socket_group=None, ):
    def __init__(self, comment="Untitled Category", show=True, **kwargs):
        self.comment = comment
        self.show = show
        # self.classes = classes
        # self.base_type = base_type
        self.attributes = {}
        for k, v in kwargs.items():
            self.attributes[k] = v
    
    def textify(self, key, to_textify):
        if type(to_textify) == list:
            return f'{key} {BaseTypeString(to_textify)}'
        elif type(to_textify) == bool:
            return f"{key} {('True' if to_textify else 'False')}"
        elif type(to_textify) == Style:
            return to_textify
        else:
            return f'{key} {to_textify}'

    def rema(self, to_remove):
        if type(to_remove) == list:
            for entry in to_remove:
                del self.attributes[to_remove]
        else:
            del self.attributes[to_remove]

    def seta(self, **kwargs):
        for k, v in kwargs.items():
            self.attributes[k] = v

    def geta(self, attrib):
        return self.attributes[attrib]

    def __str__(self):
        ret = f"{('Show' if self.show == SHOW else 'Hide')} # {self.comment}\n"
        for k, v in self.attributes.items():
            if v is not None:
                ret += indent(f'{self.textify(k,v)}\n','\t')
        return ret

    def __repr__(self):
        return self.__str__()

def testing123():
    style1 = Style(SetTextColor='34 456 544')
    filtr = FilterObj("Fun filter for family")
    cat = Category("Test Category", Class=['Scorc Boot','Hubria Cirl'], Rarity='Rare', Style=style1)
    sec = Section("Testing Section")
    sec.append(cat)
    filtr.append(sec)
    return filtr