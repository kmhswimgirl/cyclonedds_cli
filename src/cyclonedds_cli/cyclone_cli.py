import click
import os
import xml.etree.ElementTree as et
from src.cyclonedds_cli.xml_formatting import XMLFormatting as xml

prefix =  '{https://cdds.io/config}'


real_xml_path = os.getenv('CYCLONEDDS_URI')

tree = et.parse(real_xml_path)
root = tree.getroot()

ns = {'c': 'https://cdds.io/config'}  # map prefix to the namespace URI

@click.group()
def cli():
    '''A CLI tool used for managing Cyclone DDS configuration files'''

@cli.group()
def peer():
    ''' Managing peer addresses. Be sure to type the full address name when adding and removing addresses'''

@peer.command('add')
@click.argument("address")
def peer_add(address):

    # make sure <Peers> tag exists
    peers_elem = root.find('.//c:Peers', ns)
    if peers_elem is None:
        click.echo("Peers element not found", err=True)
        return
    
    # prevent adding duplicate addresses
    address = address.strip()
    existing = {p.get('address') for p in peers_elem.findall('c:Peer', ns) if p.get('address')}
    if address in existing:
        click.echo(f"{address} already exists; not adding duplicate")
        return
    
    # add the peer addr
    ns_uri = ns['c']
    new_peer = et.SubElement(peers_elem, f'{{{ns_uri}}}Peer')
    new_peer.set("address", address)

    # clean up the formatting
    et.register_namespace('', ns_uri)
    xml._normalize_whitespace(root)
    xml._indent(root)
    
    # write out
    tree.write(real_xml_path, encoding="utf-8", xml_declaration=False)
    click.echo(f"--> added {address} to the list of peers")

@peer.command('delete')
@click.argument('target')
def peer_delete(target):

    peers_elem = root.find('.//c:Peers', ns)
    if peers_elem is None:
        click.echo("Peers element not found", err=True)
        return
    
    found = None
    for p in peers_elem.findall('c:Peer', ns):
        if p.get('address') == target:
            found = p
            break

    if found is None:
        click.echo(f"{target} not found")
        return
    
    peers_elem.remove(found)

    # preserve default namespace and reformat
    et.register_namespace('', ns['c'])
    xml._normalize_whitespace(root)
    xml._indent(root)

    tree.write(real_xml_path, encoding="utf-8", xml_declaration=False)
    click.echo(f"--> removed {target} from the list of peers")
    
# command for listing all available peer addresses
@peer.command('list')
def peer_list():
    for peer in root.iter(f'{prefix}Peer'):
        print(peer.attrib.get('address'))

