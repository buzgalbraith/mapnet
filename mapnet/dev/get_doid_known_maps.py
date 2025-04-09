from deeponto.onto import Ontology, OntologyPruner

doid_path = "resources/doid.owl"
doid = Ontology(doid_path)


mesh_iri_base = "http://purl.bioontology.org/ontology/"
provided_maps = {}
mesh_map = lambda x: mesh_iri_base + x.replace(":", "/")
for iri in doid.owl_classes.keys():
    for annotation in doid.get_annotations(iri):
        if annotation.startswith("MESH:"):
            provided_maps[iri] = mesh_map(annotation.split(" ")[0])

with open("knownMaps/doid_to_mesh_provided_maps.tsv", mode="w") as f:
    f.write("SrcEntity\tTgtEntity\tScore\n")
    for doid_iri in provided_maps:
        f.write(f"{doid_iri}\t{provided_maps[doid_iri]}\t1.0\n")
