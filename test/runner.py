import os
import xmlschema
from pathlib import Path

from xsd2xml import xsd2xml

def perform_test(xsd_path: str | Path, xml_path: str | Path):
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
