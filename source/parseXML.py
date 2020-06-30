import xmltodict
import pprint
import json

with open('example.xml') as fd:
    doc = xmltodict.parse(fd.read(), process_namespaces=True)

# doc['root']['world']['walls'] = xmltodict.parse("<wall id=\"{wall1}\" begin=\"50:-50\" end=\"250:-50\"/>") # "<wall id=\"{wall1}\" begin=\"50:-50\" end=\"250:-50\"/>"

pp = pprint.PrettyPrinter(indent=4)
pp.pprint((doc))

# print(xmltodict.unparse(doc, pretty=True)) # use to write in file