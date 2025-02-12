## Make a list of known mappings between doid and DOID from the owl files. 

# from indra.databases import owl_client

# owl_clin = owl_client.OwlClient(prefix='doid')

# res = owl_clin.update_from_file(prefix='doid', file = 'resources/doid.owl')


from deeponto.onto import Ontology, OntologyPruner
from deeponto.utils import (
    InvertedIndex,
    Tokenizer,
    print_dict,
    process_annotation_literal,
    split_java_identifier,
    uniqify,
)

doid_path = 'resources/doid.owl'
doid = Ontology(doid_path)



mesh_iri_base = 'http://purl.bioontology.org/ontology/'
provided_maps = {} 
mesh_map = lambda x: mesh_iri_base+x.replace(":", "/")
for iri in doid.owl_classes.keys():
    for annotation in doid.get_annotations(iri):
        if annotation.startswith("MESH:"):
            provided_maps[iri] = mesh_map(annotation.split(" ")[0])

with open("knownMaps/doid_to_mesh_provided_maps.tsv", mode='w') as f:
    f.write("SrcEntity\tTgtEntity\tScore\n")
    for doid_iri in provided_maps:
        f.write(f"{doid_iri}\t{provided_maps[doid_iri]}\t1.0\n")
