from lxml import etree


def elem2dict(node):
    """
    Convert an lxml.etree node tree into a dict.
    """
    result = {}

    for element in node.iterchildren():
        # Remove namespace prefix
        key = element.tag.split('}')[1] if '}' in element.tag else element.tag
        key = key[:1].lower() + key[1:]

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            value = element.text
        else:
            value = elem2dict(element)
        if key in result:
            if type(result[key]) is list:
                result[key].append(value)
            else:
                tempvalue = result[key].copy()
                result[key] = [tempvalue, value]
        else:
            result[key] = value
    return result


def convert_xml_to_json(xml_text):
    tree = etree.fromstring(xml_text)
    if len(tree) > 1: # 0=Header, 1=Body
        return elem2dict(tree[1])
    return elem2dict(tree[0])
