from indra.databases import mesh_client
from deeponto.onto import Ontology, OntologyPruner
import biomappings
from deeponto.align.bertmap import BERTMapPipeline
# from biomappings.resources import append_prediction_tuples

SOURCE_PREFIX_IRI_MAPS = {
    "mesh": lambda x: "http://phenomebrowser.net/ontologies/mesh/mesh.owl#" + x,
    "mesh2024": lambda x: "http://purl.bioontology.org/ontology/MESH/" + x,
    "mesh_dissease": lambda x: "http://purl.bioontology.org/ontology/MESH/" + x,
    "doid": lambda x: "http://purl.obolibrary.org/obo/" + x.replace(":", "_"),
    "hgnc": lambda x: "https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/HGNC:" + x,
    "chebi": lambda x: "http://purl.obolibrary.org/obo/" + x.replace(":", "_"),
    "go": lambda x: "http://purl.obolibrary.org/obo/" + x.replace(":", "_"),
}
IRIsourcePrefixMaps = {
    "mesh": lambda x: x.removeprefix("http://phenomebrowser.net/ontologies/mesh/mesh.owl#"),
    "mesh2024": lambda x: x.removeprefix("http://purl.bioontology.org/ontology/MESH/"),
    "mesh_dissease": lambda x: x.removeprefix("http://purl.bioontology.org/ontology/MESH/"),
    "doid": lambda x: x.removeprefix("http://purl.obolibrary.org/obo/").replace("_", ":"),
    "hgnc": lambda x: x.removeprefix(
        "https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/"
    ),
    "chebi": lambda x: x.removeprefix("http://purl.obolibrary.org/obo/").replace("_", ":"),
    "go": lambda x: x.removeprefix("http://purl.obolibrary.org/obo/").replace("_", ":"),
}


mesh_path = 'resources/mesh2024.ttl'
mesh_dissease_path = 'resources/mesh_dissease.owl'
save_path = 'resources/mesh_dissease_new.owl'
def is_genetic(x):
    return mesh_client.has_tree_prefix(x, 'G05')
def is_chemical(x):
    return (mesh_client.has_tree_prefix(x, 'D01')) or (mesh_client.has_tree_prefix(x, 'D02'))
def filter_supplemental(mesh_path, save_path):
    mesh = Ontology(mesh_path)
    IRIs = mesh.owl_classes.keys()
    ## remove supplemental IRIs which start with C 
    suplementalFilter = lambda x: x.removeprefix(mesh.owl_iri)[0].upper() == "C"
    SuplementalIRIs = filter(suplementalFilter, IRIs)
    pruner = OntologyPruner(mesh)
    pruner.prune(list(SuplementalIRIs))
    pruner.save_onto(save_path)
def filter_non_disseases(mesh_path, save_path):
    mesh = Ontology(mesh_path)
    ## keep terms that are outside of the mesh structre to be safe
    mesh_terms = filter(lambda x: x.startswith(mesh.owl_iri), mesh.owl_classes.keys())
    ## filter for terms that are not dissaese
    not_disseases = filter(lambda x: not mesh_client.is_disease(x.removeprefix(mesh.owl_iri)), mesh_terms)
    ## drop those terms and save result
    pruner = OntologyPruner(mesh)
    pruner.prune(list(not_disseases))
    pruner.save_onto(save_path)
def filter_non_chmical(mesh_path, save_path):
    mesh = Ontology(mesh_path)
    ## keep terms that are outside of the mesh structre to be safe
    mesh_terms = filter(lambda x: x.startswith(mesh.owl_iri), mesh.owl_classes.keys())
    ## filter for terms that are not not chemical

    not_disseases = filter(lambda x: not is_chemical(x.removeprefix(mesh.owl_iri)), mesh_terms)
    ## drop those terms and save result
    pruner = OntologyPruner(mesh)
    pruner.prune(list(not_disseases))
    pruner.save_onto(save_path)
def filter_non_genetic(mesh_path, save_path):
    mesh = Ontology(mesh_path)
    ## keep terms that are outside of the mesh structre to be safe
    mesh_terms = filter(lambda x: x.startswith(mesh.owl_iri), mesh.owl_classes.keys())
    ## filter for terms that are not genetic
    not_disseases = filter(lambda x: not is_genetic(x.removeprefix(mesh.owl_iri)), mesh_terms)
    ## drop those terms and save result
    pruner = OntologyPruner(mesh)
    pruner.prune(list(not_disseases))
    pruner.save_onto(save_path)
# inference
def strip_digits(x):
    """Remove numeric characters from a string."""
    return "".join(filter(lambda x: not x.isdigit(), x))


def onto_filter(x):
    return (x["target prefix"].lower() == strip_digits(target_ontology_train.lower())) & (
        x["source prefix"].lower() == strip_digits(source_ontology_train.lower())
    )
#    filter(lambda x: not mesh_client.is_disease(x.removeprefix(mesh.owl_iri)), mesh_terms)
def iri_map(x):
    return (
        SOURCE_PREFIX_IRI_MAPS[source_ontology_train.lower()](x[0])
        + "\t"
        + SOURCE_PREFIX_IRI_MAPS[target_ontology_train.lower()](x[1])
        + "\t1.0\n"
    )

if __name__ == "__main__":


    target_ontology_train = "doid"
    mesh_path = 'resources/mesh2024.ttl'
    primary_path = "resources/mesh_primary.owl"  
    mesh_dissease_path = "resources/mesh_primary_disseae.owl"  
    mesh_chemical_path = "resources/mesh_primary_chemical.owl"  
    mesh_genetic_path = "resources/mesh_primary_genetic.owl"  
    print("filtering suplemental terms ")
    filter_supplemental(mesh_path=mesh_path, save_path=primary_path)
    print("filtering disseases")
    filter_non_disseases(mesh_path=primary_path, save_path=mesh_dissease_path)
    print("filtering chemical")
    filter_non_chmical(mesh_path=primary_path, save_path=mesh_chemical_path)
    print("filtering genetic")
    filter_non_genetic(mesh_path=primary_path, save_path=mesh_genetic_path)

    ## load in ontologies 
    # target_ontology_train = "doid"
    # source_ontology_train = "mesh2024"
    # src_onto = Ontology('resources/mesh_dissease_new.owl')
    # print("loading mesh")

    # target_onto = Ontology('resources/doid.owl')
    # print("loading doid")



    ## write out known mappings
    # known_maps_path = "knownMaps/mesh_dissease-doid.tsv"
    # true_mappings = biomappings.load_mappings()
    # a = filter(onto_filter, true_mappings)
    # val_mapping = lambda x:(x["source identifier"], x["target identifier"])
    # b = map(val_mapping, a)
    # disease_filter = lambda x: not mesh_client.is_disease(x[0].removeprefix(src_onto.owl_iri))
    # # chemical_filter = lambda x: not is_chemical(x[0].removeprefix(src_onto.owl_iri))
    
    # c = filter(disease_filter, b)
    # d = map(iri_map, c)


    # with open(known_maps_path, mode= 'w') as f:
    #     f.write("SrcEntity\tTgtEntity\tScore\n")
    #     for row in d:
    #         f.write(row)
    # ## set up model config
    # config_file = "mapnet/bertmap/config/bertmap_config.yaml"
    # config = BERTMapPipeline.load_bertmap_config(config_file)
    # config.known_mappings = known_maps_path
    # config.global_matching.enabled = False
    # ## train model 
    # BERTMapPipeline(src_onto, target_onto, config)

