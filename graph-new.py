import xml.etree.ElementTree as ET
import datetime


def find_all_sub_ways(way, sub_ways_et, graph_root):
    way_name = "none"
    for tag in way.findall("tag"):
        tag_type = tag.get("k")
        if tag_type == "name":
            way_name = tag.get("v")
            break

    for sub_way in graph_root.iter("way"):
        if sub_way == way:
            continue
        sub_way_tags = sub_way.findall("tag")
        for tag in sub_way_tags:
            tag_type = tag.get("k")
            if tag_type == "name":
                if tag.get("v") == way_name:
                    sub_way_nds = sub_way.findall("nd")
                    sub_way_nds_id = [tmp.get("ref") for tmp in sub_way_nds]
                    way_nds_id = [tmp.get("ref") for tmp in way.findall("nd")]
                    intersection = list(set(sub_way_nds_id) & set(way_nds_id))
                    if ((len(intersection) != 0) and (way_name == "nan")) or (way_name != "nan"):
                        for nd in sub_way_nds:
                            if nd.get("id") not in intersection:
                                way.append(nd)
                            sub_ways_et.append(sub_way)
                continue


def way_to_node(graph_root, sub_root, keys):
    print("way->node")
    sub_ways_et = []
    for way in graph_root.iter("way"):
        if way in sub_ways_et:
            continue

        find_all_sub_ways(way, sub_ways_et, graph_root)
        node = ET.SubElement(sub_root, "node")
        way_id = way.get("id", None)
        node.set("id", way_id)

        for tag in way.iter("tag"):
            tag_type = tag.get("k", None)
            if tag_type in keys:
                data = node.makeelement("data", {"key": str(tag_type)})
                node.append(data)
                value = tag.get("v", None)
                data.text = value

    return sub_ways_et


def node_to_edge(graph_root, sub_root):
    print("node->edge")
    for node in graph_root.iter("node"):
        node_id = node.get("id", None)
        way_list = []
        for way in graph_root.iter("way"):
            way_id = way.get("id", None)
            node.set("id", way_id)
            for nd in way.iter("nd"):
                ref = nd.get("ref")
                if ref == node_id:
                    way_list.append(way_id)
                    break

        way_list_copy = way_list.copy()
        ed = [[a, b] for a in way_list for b in way_list_copy if a != b]
        edges = []

        for edge in ed:
            if [edge[1], edge[0]] not in edges:
                edges.append(edge)

        for points in edges:
            edge = ET.SubElement(sub_root, "edge")
            edge.set("id", str(points[0])+"-"+str(points[1]))
            edge.set("source", points[0])
            edge.set("target", points[1])


def delete_sub_ways(sub_ways_et, graph_root):
    for et in sub_ways_et:
        try:
            graph_root.remove(et)
        except:
            y = 1


def creating_graphs(inputfile, attrib):
    input_graph = ET.parse(inputfile)
    input_graph_root = input_graph.getroot()
    reversed_graph_root = ET.Element("graphml")
    reversed_graph = ET.ElementTree(reversed_graph_root)

    for atr, value in attrib:
        key = reversed_graph_root.makeelement('key', atr)
        reversed_graph_root.append(key)
        default = key.makeelement('default', {})
        key.append(default)
        default.text = value

    sub_root = reversed_graph_root.makeelement('graph', {"edgedefault": "undirected"})
    reversed_graph_root.append(sub_root)

    return input_graph, input_graph_root, reversed_graph, reversed_graph_root, sub_root


def rebuilding_graph(inputfile, outputfile):
    start = datetime.datetime.now()
    keys, attrib = attributes()

    input_graph, input_graph_root, reversed_graph, reversed_graph_root, sub_root = creating_graphs(inputfile, attrib)
    now = datetime.datetime.now()
    print("work-time creating_graphs: ", now-start)

    sub_ways_et = way_to_node(input_graph_root, sub_root, keys)
    now = datetime.datetime.now()
    print("work-time way_to_node: ", now-start)

    delete_sub_ways(sub_ways_et, input_graph_root)

    node_to_edge(input_graph_root, sub_root)
    now = datetime.datetime.now()
    print("work-time node_to_edge: ", now-start)

    reversed_graph.write(outputfile)
    now = datetime.datetime.now()
    print("work-time: ", now-start)


def attributes():
    keys = ('highway', 'lanes', 'maxspeed', 'surface', 'bicycle', 'name', 'oneway')
    attrib = [({'id': keys[0], "for": "node", "attr.name": "highway", "attr.type": "string"}, 'undefined'),
              ({'id': keys[1], "for": "node", "attr.name": "lanes", "attr.type": "string"}, 'undefined'),
              ({'id': keys[2], "for": "node", "attr.name": "maxspeed", "attr.type": "string"}, 'undefined'),
              ({'id': keys[3], "for": "node", "attr.name": "surface", "attr.type": "string"}, 'asphalt'),
              ({'id': keys[4], "for": "node", "attr.name": "bicycle", "attr.type": "string"}, 'no'),
              ({'id': keys[5], "for": "node", "attr.name": "name", "attr.type": "string"}, 'undefined'),
              ({'id': keys[6], "for": "node", "attr.name": "oneway", "attr.type": "string"}, 'no')]
    return keys, attrib


def main():
    rebuilding_graph(inputfile='kaliningradroads.osm', outputfile='reversed-kaliningradroads-2.graphml')


if __name__ == '__main__':
    main()
