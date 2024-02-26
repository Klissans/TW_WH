import os
import re

from bs4 import BeautifulSoup

soupFactory = BeautifulSoup("<b></b>", 'html.parser')


def find_by_name(xml, name):
    r = xml.find_all(lambda t: t.name == name)
    if len(r) == 0:
        raise Exception(f'Name {name} is missing')
    if len(r) > 1:
        raise Exception(f'Name {name} is not unique')
    return r[0]


def find_by(xml, attr_name: str, value: str):
    fn = lambda t: t.has_attr(attr_name) and t[attr_name] == value
    r = xml.find_all(fn)
    if len(r) == 0:
        raise Exception(f'{attr_name} {value} is missing')
    if len(r) > 1:
        raise Exception(f'{attr_name} {value} is not unique')
    return r[0]


def find_by_id(xml, id: str):
    return find_by(xml, 'id', id)


def find_by_guid(xml, guid: str):
    return find_by(xml, 'uniqueguid', guid)


def find_by_callback_id(xml, callback_id: str):
    return find_by(xml, 'callback_id', callback_id)


def replace_escape_characters(s: str):
    return s.replace('&lt;', '%%lt%%').replace('&gt;', '%%gt%%').replace('&quot;', '%%quot%%').replace('&amp;', '%%amp%%')


def destroy_element(xml, guid):
    find_by_guid(xml, guid).decompose()
    find_by(xml, 'this', guid).decompose()

def read_twui(fp: str, is_custom=False):
    path = f'xmls/twui/{fp}.twui.xml' if is_custom else f'../../data/{fp}.twui.xml'
    with open(path) as f:
        text = replace_escape_characters(f.read())
    
    pattern = r'&[^;]+;'
    matches = re.findall(pattern, text)
    print(set(matches))
    return text


def read_xml_component(fp: str):
    with open(f'xmls/components/{fp}.xml') as f:
        text = replace_escape_characters(f.read())
    elem = BeautifulSoup(text, 'lxml-xml').contents[0]
    return elem


def write(fp: str, xml):
    output = f'output/{fp}.twui.xml'
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        f.write(xml.prettify(formatter=None).replace('%%lt%%', '&lt;').replace('%%gt%%', '&gt;').replace('%%quot%%',
                                                                                                         '&quot;').replace(
            '%%amp%%', '&amp;'))


def edit_twui(fp: str, fn):
    is_custom = '/mod/' in fp
    xml = BeautifulSoup(read_twui(fp, is_custom), 'lxml-xml')
    fn(xml)
    write(fp, xml)


def format_str(s: str):
    return s.replace('<', '%%lt%%').replace('>', '%%gt%%').replace('"', '%%quot%%').replace('&', '%%amp%%')


def add_element(xml, elem, where):
    find_by_name(xml.layout.hierarchy, where).append(soupFactory.new_tag(elem.name, this=elem["this"]))
    xml.layout.components.append(elem)


def insert_after_element(xml, elem, where):
    find_by_name(xml.layout.hierarchy, where).insert_after(soupFactory.new_tag(elem.name, this=elem["this"]))
    xml.layout.components.append(elem)


def add_element_from_string(xml, desc, where):
    elem = BeautifulSoup(desc, 'lxml-xml').contents[0]
    find_by_name(xml.layout.hierarchy, where).append(soupFactory.new_tag(elem.name, this=elem["this"]))
    xml.layout.components.append(elem)


def insert_after_element_from_string(xml, desc, where):
    elem = BeautifulSoup(desc, 'lxml-xml').contents[0]
    find_by_name(xml.layout.hierarchy, where).insert_after(soupFactory.new_tag(elem.name, this=elem["this"]))
    xml.layout.components.append(elem)


def set_context_callback(elem, callback_id: str, context_function: str):
    tag = find_by_callback_id(elem, callback_id)
    tag['context_function_id'] = format_str(context_function)
    return tag


def create_properties(properties):
    sp = ''
    # TODO string concat
    for k, v in properties.items():
        sp += f'<property name="{k}" value="{v}"/>'
    return sp


def create_context_callback_as_string(id, object=None, function=None, properties=None):
    props_s = ''
    if properties:
        props_s = f'<child_m_user_properties>{create_properties(properties)}</child_m_user_properties>'
    
    if object is None and function is None:
        desc = f'<callback_with_context callback_id="{id}"/>'
    elif object is None or function is None:
        raise Exception('Wrong arguments')
    else:
        desc = f'''
            <callback_with_context
                callback_id="{id}"
                context_object_id="{object}"
                context_function_id="{format_str(function)}">
                {props_s}
            </callback_with_context>
        '''
    return desc

