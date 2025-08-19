from pyvis.network import Network

def build_pyvis_graph(triples, existing_nodes=None, existing_edges=None):
    net = Network(height="700px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    net.barnes_hut()

    if existing_nodes is None:
        existing_nodes = set()
    if existing_edges is None:
        existing_edges = set()

    node_set = existing_nodes.copy()
    edge_set = existing_edges.copy()

    # Collect all new nodes to optionally style them differently
    new_nodes = set()

    for triple in triples:
        subj = triple["subject"].strip().lower()
        obj  = triple["object"].strip().lower()
        rel  = triple["relation"].strip().lower()

        # Track new nodes
        if subj not in node_set:
            new_nodes.add(subj)
        if obj not in node_set:
            new_nodes.add(obj)

        # Add subject node
        net.add_node(subj, label=subj, title=subj,
                     color="#FF4C4C" if subj in new_nodes else "#32CD32")  # red or green

        # Add object node
        net.add_node(obj, label=obj, title=obj,
                     color="#FF4C4C" if obj in new_nodes else "#32CD32")  # red or green

        # Add edge if not already present
        edge_key = (subj, obj, rel)
        if edge_key not in edge_set:
            net.add_edge(subj, obj, label=rel, title=rel)
            edge_set.add(edge_key)

        # Update sets to reflect what's added
        node_set.add(subj)
        node_set.add(obj)

    return net, node_set, edge_set
