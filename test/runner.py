import os
import xmlschema
from pathlib import Path

from src.xsd2xml import xsd2xml


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def perform_test(xsd_path: str | Path, xml_path: str | Path):
    xsd_path = get_project_root() / 'test' / xsd_path
    xml_path = get_project_root() / 'test' / xml_path

    # Load XSD, generate & save XML.
    xml_gen = xsd2xml.Xsd2Xml(xsd_path)
    xml_gen.gen_xml()
    xml_gen.save_xml(xml_path)

    # Validate XML against XSD.
    xs = xmlschema.XMLSchema(xsd_path)
    res = xs.is_valid(xml_path)

    # Remove stray XML file.
    os.remove(xml_path)

    # Return validation result.
    return res
