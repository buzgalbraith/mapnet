from deeponto.onto import Ontology, OntologyPruner
from deeponto.utils import (
    InvertedIndex,
    Tokenizer,
    print_dict,
    process_annotation_literal,
    split_java_identifier,
    uniqify,
)

mesh_path = 'resources/MESH_BASE.owl'
mesh = Ontology(mesh_path)


## try filtering using data properties
#mesh.owl_classes
entity_type = "DataProperties"
entity_type = "owl_" + split_java_identifier(entity_type).replace(" ", "_").lower()
entity_index = getattr(mesh, entity_type)
## filtter for non-supplemental 
suplementalFilter = lambda x: x.removeprefix(mesh.owl_iri)[0].upper() != "C"
res = {x:entity_index[x] for x in entity_index.keys() if suplementalFilter(x)}


# preserve available annotation properties
annotation_property_iris = mesh.owl_annotation_properties.keys()
annotation_property_iris = [
    airi for airi in annotation_property_iris if airi in mesh.owl_annotation_properties.keys()
]

CUI_AIRI = "http://bioportal.bioontology.org/ontologies/umls/cui"
map_func = lambda x: mesh.get_annotations(
                            owl_object=res[x],
                            annotation_property_iri=CUI_AIRI,) 

DisCheck = lambda x: any([y.startswith("C") for y in x])

WithCUI = {x:map_func(x) for x in res.keys()}
WithCUIDis = {x:map_func(x) for x in res.keys() if not DisCheck(map_func(x))}

for iri, entity in res.items(): 
    print(entity)
    for airi in annotation_property_iris:
        print(airi)
        val = mesh.get_annotations(
                            owl_object=entity,
                            annotation_property_iri=airi,
                            annotation_language_tag=None,
                            apply_lowercasing=True,
                            normalise_identifiers=False)
        print(val)
    break


entity_type = "DataProperties"
entity_type = "owl_" + split_java_identifier(entity_type).replace(" ", "_").lower()
entity_index = getattr(mesh, entity_type)
for iri, entity in entity_index.items(): 
    entity = entity_index['http://purl.bioontology.org/ontology/MESH/MN']
    print(entity)
    for airi in annotation_property_iris:
        print(airi)
        val = mesh.get_annotations(
                            owl_object=entity,
                            annotation_property_iri=airi,
                            annotation_language_tag=None,
                            apply_lowercasing=True,
                            normalise_identifiers=False)
        print(val)
    break
