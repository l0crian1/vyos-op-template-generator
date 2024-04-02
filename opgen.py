import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def add_node_with_attributes(current_node, part, root, nodeType):
    """Parse part with potential attributes and add to current_node."""
    part_name = part[0]  # Assuming it's always within <>
    children = ET.SubElement(current_node, "children") if current_node != root else current_node
    current_node = ET.SubElement(children, nodeType, name=part_name)

    for item in part[1:]:
        if ':' in item and not ':=' in item:
            subvalues = item.split(':')
            children = ET.SubElement(current_node, subvalues[0])                    
            for i in subvalues:
                if i:
                    if '=' in i:
                        for j in i.split(','):                        
                            if '=' in j:
                                sub_key, sub_value = j.split("=")
                                ET.SubElement(children, sub_key).text = sub_value
                    else:
                        if i != subvalues[0]:
                            children = ET.SubElement(children, i)
        elif ':=' in item:
            tmp = item.split(':=')
            children = ET.SubElement(current_node, tmp[0]).text = tmp[1]
        else:
            pass
    return current_node

def create_xml_structure(command):
    parts = command.split('//')

    root = ET.Element("interfaceDefinition")
    current_node = root
    for part in parts:
        if part.startswith('<'):  # Adjust this condition as needed for broader applicability
            part = part.replace('<','').replace('>','')
            if '@' in part:
                part = part.split('@')
            current_node = add_node_with_attributes(current_node, part, root, 'tagNode')
        elif part.startswith('!'):
            part = part[1:]  # leafNode
            if '@' in part:
                part = part.split('@')
            current_node = add_node_with_attributes(current_node, part, root, 'leafNode')
            break  # No further nodes after a leafNode
        else:  # Regular node
            if '@' in part:
                part = part.split('@')
                current_node = add_node_with_attributes(current_node, part, root, 'node')
            else:
                # This handles regular nodes without any special attributes
                if current_node == root:
                    current_node = ET.SubElement(current_node, "node", name=part)
                else:
                    children = current_node if current_node.tag == "children" else ET.SubElement(current_node, "children")
                    current_node = ET.SubElement(children, "node", name=part)


    return prettify_xml(root)

# Example usage
command_input = input("Enter your command: ")
print('')
xml_structure = create_xml_structure(command_input)
print(xml_structure)
