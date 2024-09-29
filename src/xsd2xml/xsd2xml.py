import string
import random
from pathlib import Path
from typing import Type

import rstr
import xmlschema
from xmlschema.validators import (XsdGroup, XsdElement, XsdAnyElement, XsdSimpleType, XsdComplexType,
                                  XsdAtomicRestriction, XsdTotalDigitsFacet, XsdFractionDigitsFacet,
                                  XsdMinInclusiveFacet, XsdPatternFacets, XsdEnumerationFacets, XsdMaxLengthFacet,
                                  XsdMinLengthFacet)
import xml.etree.cElementTree as et


INT_LIMIT = 999_999_999
FLOAT_LIMIT = 999_999_999.999_999_999


class Xsd2Xml:
    def __init__(self, xsd_path: str | Path):
        self.xsd_path = xsd_path

        self.root: Type[et.Element]
        self.root = None

        self.schema: Type[xmlschema.XMLSchema]
        self.schema = None

    @staticmethod
    def rand_decimal(int_digs: int, frac_digs: int) -> float:
        value = random.randint((10 ** (int_digs - 1)), ((10 ** int_digs) - 1))
        int_part = random.choice([-value, value])
        frac_part = random.randint((10 ** (frac_digs - 1)), ((10 ** frac_digs) - 1))
        return float('.'.join([str(int_part), str(frac_part)]))

    @staticmethod
    def random_date(with_time=False, with_timezone=False) -> str:
        def gen_month_day(mon: int) -> int:
            if mon in [1, 3, 5, 7, 8, 10, 12]:
                return random.randint(1, 31)
            elif mon in [4, 6, 9, 11]:
                return random.randint(1, 30)
            elif mon in [2]:
                return random.randint(1, 28)
            else:
                return 0

        year = random.randint(1900, 2100)
        month = random.randint(1, 12)
        day = gen_month_day(month)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        timezone = random.randint(-12, 12)
        value = f'{year}-{month:02d}-{day:02d}'
        value += f'T{hour:02d}:{minute:02d}:{second:02d}' if with_time else ''
        value += f'{timezone:+03d}:00' if with_timezone else ''
        return value

    @staticmethod
    def get_restriction(elem: XsdAtomicRestriction | XsdSimpleType | XsdComplexType) -> dict:
        restr = {}

        print('elem', elem)

        if hasattr(elem, 'type'):
            base_type = elem.type
        else:
            base_type = elem

        for fac in base_type.facets.values():
            if isinstance(fac, XsdTotalDigitsFacet):
                restr['total_dig'] = fac.value
            elif isinstance(fac, XsdFractionDigitsFacet):
                restr['frac_dig'] = fac.value
            elif isinstance(fac, XsdMinInclusiveFacet):
                restr['min_incl'] = fac.value
            elif isinstance(fac, XsdPatternFacets):
                restr['patterns'] = [p for p in fac.regexps]
            elif isinstance(fac, XsdEnumerationFacets):
                restr['enums'] = [e for e in fac.enumeration]
            elif isinstance(fac, XsdMaxLengthFacet):
                restr['maxLen'] = fac.value
            elif isinstance(fac, XsdMinLengthFacet):
                restr['minLen'] = fac.value

        print('restr', restr)

        return restr

    # Resolve the base type (custom or built-in)
    def resolve_base_type(self, elem_type):
        base_type = elem_type.base_type if elem_type.base_type is not None else elem_type

        # If the base type is a reference to another custom type, resolve it
        while base_type and base_type.is_derived:
            base_type = self.schema.types[base_type.base_type.name]

        return base_type

    def gen_group(self, parent: et.Element, group: XsdGroup):
        if group.model == 'choice':
            self.gen_element(parent, random.choice(group))
        else:
            for c in group:
                self.gen_element(parent, c)

    @staticmethod
    def gen_attr(xml_elem: et.Element, elem: XsdElement):
        for attr_name, attr_info in elem.attributes.items():
            # Generate random data for the attribute based on its type
            xml_elem.set(attr_name, 'ASD')

    def get_type(self, elem: XsdElement, restr=None) -> [str | dict]:
        base_types = ['string', 'decimal', 'integer', 'positiveInteger', 'dateTime', 'date']
        if elem.type.local_name in base_types:
            # name = strip_ns(elem.type.name)
            name = elem.type.local_name
        elif elem.type.base_type.name is not None:
            # name = strip_ns(elem.type.base_type.name)
            name = elem.type.base_type.local_name
            if name not in base_types:
                base_type = elem.type
                name = base_type.local_name
                while name not in base_types:
                    base_type = base_type.base_type
                    name = base_type.local_name
                    if isinstance(base_type, XsdAtomicRestriction):
                        restr = self.get_restriction(self.schema.types[name])
        else:
            name = ''

        return name, restr

    def gen_value(self, xml_elem: et.Element, elem: XsdElement, restr=None):
        if restr is None:
            restr = {}

        name, restr = self.get_type(elem, restr)

        value = ''

        if name == 'string':
            value = ''.join(random.choice(string.ascii_letters) for _ in range(32))
            if 'patterns' in restr:
                value = rstr.xeger(random.choice(restr['patterns']))
                if 'maxLen' in restr:
                    value = value[:restr['maxLen']]
            elif 'enums' in restr:
                value = random.choice(restr['enums'])
            elif 'maxLen' in restr and 'minLen' in restr:
                length = random.randint(restr['minLen'], restr['maxLen'])
                value = ''.join(random.choice(string.ascii_letters) for _ in range(length))
            elif 'maxLen' in restr:
                value = 'a' * restr['maxLen']
            elif 'minLen' in restr:
                value = 'b' * restr['minLen']
        elif name == 'positiveInteger':
            value = str(random.randint(0, INT_LIMIT))
        elif name == 'integer':
            value = str(random.randint(-INT_LIMIT, INT_LIMIT))
        elif name == 'decimal':
            min_incl = restr.get('min_incl', float('-inf'))  # Use -inf as default minimum.
            frac_dig = restr.get('frac_dig', 1)
            int_dig = restr.get('total_dig', 1) - frac_dig
            print(restr)
            print(frac_dig, int_dig)
            value = str(max(min_incl, self.rand_decimal(int_dig, frac_dig)))
        elif name == 'dateTime':
            value = self.random_date(True, True)
        elif name == 'date':
            value = self.random_date(False, True)
        else:
            print('unknown element:', name)

        xml_elem.text = value

        self.gen_attr(xml_elem, elem)

    def gen_restriction_value(self, xml_elem: et.Element, elem: XsdElement):
        restr = self.get_restriction(elem.type)
        self.gen_value(xml_elem, elem, restr)

    def gen_element_type(self, xml_elem: et.Element, elem: XsdElement):
        if isinstance(elem.type, XsdAnyElement):
            pass
        elif isinstance(elem.type, XsdComplexType):
            if elem.type.model_group is not None:
                self.gen_group(xml_elem, elem.type.model_group)
            else:
                self.gen_value(xml_elem, elem)
        elif isinstance(elem.type, XsdSimpleType):
            if isinstance(elem.type, XsdAtomicRestriction):
                self.gen_restriction_value(xml_elem, elem)
            else:
                self.gen_value(xml_elem, elem)

    def gen_element(self, parent: et.Element, elem: XsdElement):
        # Always at least 1 element.
        min_occurs = max(elem.min_occurs, 1)
        for i in range(min_occurs):
            xml_elem = et.SubElement(parent, elem.name)
            self.gen_element_type(xml_elem, elem)

    def __gen_xml(self, root: XsdElement):
        parent = et.Element(root.name)
        self.gen_element_type(parent, root)
        return parent

    def gen_xml(self):
        self.schema = xmlschema.XMLSchema(self.xsd_path)
        self.root = self.__gen_xml(self.schema.root_elements[0])
        return self.root

    def save_xml(self, xml_path: str | Path):
        tree = et.ElementTree(self.root)
        et.indent(tree)
        tree.write(xml_path)
