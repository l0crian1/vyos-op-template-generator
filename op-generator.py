import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def add_node_with_attributes(current_node, part, root, nodeType):
    """Parse part with potential attributes and add to current_node."""
    # Ensure 'part' has at least one element to prevent index errors
    if not part:
        print("Warning: Empty part detected. Skipping.")
        return current_node

    part_name = part[0]  # Extract the node's name
    # Create 'children' element only when necessary to avoid empty 'children' elements
    if current_node != root or nodeType != "node":
        children = ET.SubElement(current_node, "children")
    else:
        children = current_node
    current_node = ET.SubElement(children, nodeType, name=part_name)

    for item in part[1:]:
        # Split on the first occurrence of ':=' to correctly handle values that contain ':='
        if ':=' in item:
            key, value = item.split(':=', 1)
            ET.SubElement(current_node, key).text = value
        elif ':' in item:
            try:
                subvalues = item.split(':')
                sub_node = ET.SubElement(current_node, subvalues[0])
                # Process each attribute, split on the first '=' to handle values containing '='
                for attr in subvalues[1:]:
                    attr_key, attr_value = attr.split('=', 1)
                    ET.SubElement(sub_node, attr_key).text = attr_value
            except ValueError as e:
                print(f"Error processing attributes for {item}: {e}")
        else:
            print(f"Unrecognized item format: {item}")

    return current_node

def create_xml_structure(command):
    parts = command.split('//')

    root = ET.Element("interfaceDefinition")
    current_node = root
    for part in parts:
        if '@' in part:
            # Split part on the first '@' to handle parts containing '@'
            split_part = part.split('@', 1)
            part_name = split_part[0].strip('<>')
            attributes = split_part[1] if len(split_part) > 1 else ""
            part = [part_name] + attributes.split('@')
        else:
            part = [part.strip('<>')]
        
        # Determine the node type based on its prefix
        nodeType = "node"
        if part[0].startswith('!'):
            nodeType = "leafNode"
            part[0] = part[0][1:]  # Remove the prefix
        elif part[0] != part[0].strip('<>'):
            nodeType = "tagNode"

        current_node = add_node_with_attributes(current_node, part, root, nodeType)
        # Stop processing further nodes if a leafNode is encountered
        if nodeType == "leafNode":
            break

    return prettify_xml(root)

# Example usage
try:
    command_input = input("Enter your command: ")
    xml_structure = create_xml_structure(command_input)
    print(xml_structure)
except Exception as e:
    print(f"An error occurred: {e}")
