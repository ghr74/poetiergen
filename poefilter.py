import copy
from collections import defaultdict
from textwrap import dedent, indent
from typing import Any, Callable, DefaultDict, Dict, Iterator, List, Optional, Union
from poepy_core import BaseTypeString

SHOW = 1
HIDE = 2
DISABLE = 3


def CustomSound(name, atype: str = "mp3"):
    return f'"{name}.{atype}"'


class Style:

    STYLEOPS = {
        "SetFontSize",
        "SetTextColor",
        "SetBackgroundColor",
        "SetBorderColor",
        "MinimapIcon",
        "PlayEffect",
        "PlayAlertSound",
        "CustomAlertSound",
    }

    def __init__(
        self,
        SetFontSize: int = 45,
        SetTextColor: str = None,
        SetBackgroundColor: str = None,
        SetBorderColor: str = None,
        MinimapIcon: str = None,
        PlayEffect: str = None,
        PlayAlertSound: str = None,
        CustomAlertSound: str = None,
    ) -> None:
        self.attributes: Dict[str, Any] = {}
        self.attributes["SetFontSize"] = SetFontSize
        self.attributes["SetTextColor"] = SetTextColor
        self.attributes["SetBackgroundColor"] = SetBackgroundColor
        self.attributes["SetBorderColor"] = SetBorderColor
        self.attributes["MinimapIcon"] = MinimapIcon
        self.attributes["PlayEffect"] = PlayEffect
        self.attributes["PlayAlertSound"] = PlayAlertSound
        self.attributes["CustomAlertSound"] = CustomAlertSound

    def textify(self, key: str, to_textify: Any) -> str:
        if type(to_textify) == list:
            return f"{key} {BaseTypeString(to_textify)}"
        elif type(to_textify) == bool:
            return f"{key} {('True' if to_textify else 'False')}"
        else:
            return f"{key} {to_textify}"

    def __str__(self) -> str:
        ret = ""
        for att, val in self.attributes.items():
            ret += f"{self.textify(att, val)}\n" if val is not None else ""
        return ret.strip()

    def __repr__(self) -> str:
        return self.__str__()

    def changed_copy(self, **kwargs):
        ret = copy.deepcopy(self)
        for k, v in kwargs.items():
            ret.attributes[k] = v
        return ret


class Category:
    # def __init__(self, comment="Untitled Category", show=True, classes=None, base_type=None, rarity=None, sockets=None, linked_sockets=None, socket_group=None, ):
    def __init__(
        self,
        comment: str = "Untitled Category",
        show: int = SHOW,
        tags: List[str] = [],
        **kwargs,
    ):
        self.comment = comment
        self.show = show
        self.tags = tags
        self.attributes: Dict[str, Any] = {}
        for k, v in kwargs.items():
            self.attributes[k] = v

    def textify(self, key: str, to_textify: Any):
        if type(to_textify) == list:
            return f"{key} {BaseTypeString(to_textify)}"
        elif type(to_textify) == bool:
            return f"{key} {('True' if to_textify else 'False')}"
        elif type(to_textify) == Style:
            return to_textify
        else:
            return f"{key} {to_textify}"

    def rema(self, to_remove):
        if type(to_remove) == list:
            for entry in to_remove:
                del self[to_remove]
        else:
            del self[to_remove]

    def __delitem__(self, key: str) -> None:
        del self.attributes[key]

    def __getitem__(self, key: str) -> Any:
        return self.attributes.get(key)

    def get_base_type(self) -> List[str]:
        return self.attributes.get("BaseType", [])

    def __setitem__(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def seta(self, args: List[tuple]) -> None:
        for (k, v) in args:
            self[k] = v

    def geta(self, attrib: str) -> Any:
        return self[attrib]

    def __str__(self):
        ret = f"{('Show' if self.show == SHOW else 'Hide')} # {self.comment}{''.join([f' ~ {tag}' for tag in self.tags])}\n"
        for k, v in self.attributes.items():
            if v is not None:
                ret += indent(f"{self.textify(k,v)}\n", "\t")
        return ret

    def __repr__(self):
        return self.__str__()


class Section:
    def __init__(
        self,
        comment: str = "UNTITLED SECTION",
        tags: List[str] = [],
        *initial_categories,
    ) -> None:
        self.comment = comment
        self.tags = tags
        self.categories: Dict[str, Category] = {}
        for category in initial_categories:
            self.append(category)

    def append(self, category) -> None:
        self.categories[category.comment] = category

    def __len__(self) -> int:
        return len(self.categories)

    def __getitem__(self, key: str) -> Category:
        if key in self.categories:
            return self.categories[key]
        else:
            raise KeyError

    def __setitem__(self, key: str, value: Category) -> None:
        self.categories[key] = value

    def __str__(self) -> str:
        ret = ""
        ret += f'#{"---"*36}\n'
        ret += f"# Section:\t#\t{self.comment}{''.join([f' ~ {tag}' for tag in self.tags])}\n"
        ret += f'#{"---"*36}\n'
        for category in self.categories.values():
            if category.show != DISABLE:
                ret += indent(f"{category}", "\t")
        return ret

    def __repr__(self) -> str:
        return self.__str__()


class FilterObj:
    def __init__(self, comment: str = "Filter header comment") -> None:
        self.sections: Dict[str, Section] = {}
        self.styles: List[Style] = []
        self.tags: DefaultDict[str, List[Union[Category, Section]]] = defaultdict(list)
        self.comment = comment

    @staticmethod
    def from_file(source_file: str) -> "FilterObj":
        current_filter: Optional[FilterObj] = None
        with open(source_file, "r") as source_fp:
            lines = [l.strip() for l in source_fp]
            current_section: Optional[Section] = None
            current_category: Optional[Category] = None
            for line in lines:
                if "# Filter:" in line:
                    current_filter = FilterObj(line.replace("# Filter:\t#\t", ""))
                elif "# Section:" in line:
                    if all(c is not None for c in {current_category, current_section}):
                        current_section.append(current_category)  # type: ignore
                    if current_section is not None:
                        current_filter.append(current_section)  # type: ignore
                        current_section = None
                        current_category = None
                    line_args: List[str] = line.replace("# Section:\t#\t", "").split(
                        " ~ "
                    )
                    sec_name, sec_tags = line_args[0], line_args[1:]
                    current_section = Section(sec_name, tags=sec_tags)
                    for tag in sec_tags:
                        current_filter.tags[tag].append(current_section)  # type: ignore
                elif line.startswith("#"):
                    pass
                else:
                    val: Union[str, List[str]]
                    com, val = line.split(" ", 1)
                    if any(c in com for c in {"Show", "Hide"}):
                        if all(
                            c is not None for c in {current_category, current_section}
                        ):
                            current_section.append(current_category)  # type: ignore
                            current_category = None
                        val = val.replace("# ", "").split(" ~ ")  # type: ignore
                        cat_name, cat_tags = val[0], val[1:]
                        current_category = Category(
                            cat_name, (1 if "Show" in com else 2), tags=cat_tags
                        )
                        for tag in cat_tags:
                            current_filter.tags[tag].append(  # type: ignore
                                current_category
                            )
                    else:
                        if '"' in val:
                            val = [x.strip('"') for x in val.split('" "')]
                        current_category.attributes[com] = val  # type: ignore
            current_section.append(current_category)  # type: ignore
            current_filter.append(current_section)  # type: ignore
        if current_filter is None:
            current_filter = FilterObj()
        return current_filter

    def append(self, section: Section) -> None:
        self.sections[section.comment] = section

    def exception_from_section(self, section_name: str) -> List[Category]:
        return [
            cat
            for cat in self[section_name].categories.values()
            if "Exception" in cat.comment
        ]

    def basetypes_from_tag(self, tag: str) -> List[str]:
        ret: List[str] = []
        for tagged in self.tags[tag]:
            if isinstance(tagged, Category):
                ret.extend(tagged.get_base_type())
        return ret

    def apply_to_tag(
        self, tag: str, fun: Callable[[Union[Category, Section]], None]
    ) -> None:
        for tagged in self.tags[tag]:
            fun(tagged)

    def __len__(self) -> int:
        return len(self.sections)

    def __getitem__(self, key: str) -> Section:
        if key in self.sections:
            return self.sections[key]
        else:
            raise KeyError

    def __setitem__(self, key: str, value: Section) -> None:
        self.sections[key] = value

    def __str__(self) -> str:
        ret = f"# Filter:\t#\t{self.comment}\n"
        for section in self.sections.values():
            ret += f"{section}"
        return ret

    def __repr__(self) -> str:
        return self.__str__()
