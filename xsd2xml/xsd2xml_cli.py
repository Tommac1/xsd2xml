#!/usr/bin/env python3

import argparse
import xmlschema

from xsd2xml import xsd2xml


def validate(xsd_path: str, xml_path: str):
    xs = xmlschema.XMLSchema(xsd_path)
    xs.validate(xml_path)


def parse_args() -> [str, str]:
    parser = argparse.ArgumentParser(prog='Xsd2Xml', description='Generate XML from XSD schema file.')
    parser.add_argument('xsd_path', help='Path to XSD schema file.')
    parser.add_argument('xml_path', help='Path to generated XML file.')

    args = parser.parse_args()
    return args.xsd_path, args.xml_path


def main():
    xsd_path, xml_path = parse_args()

    xml_gen = xsd2xml.Xsd2Xml(xsd_path)
    xml_gen.gen_xml()
    xml_gen.save_xml(xml_path)

    validate(xsd_path, xml_path)


if __name__ == '__main__':
    main()
