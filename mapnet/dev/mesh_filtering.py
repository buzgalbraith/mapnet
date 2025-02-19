from indra.databases import mesh_client
from deeponto.onto import Ontology, OntologyPruner
import biomappings
from deeponto.align.bertmap import BERTMapPipeline

# from biomappings.resources import append_prediction_tuples
from mapnet.bertmap.generate_bertmap_predictions import get_iri_overload


save_path = "resources/mesh_dissease_new.owl"


def is_genetic(x):
    return mesh_client.has_tree_prefix(x, "G05")


def is_chemical(x):
    return (mesh_client.has_tree_prefix(x, "D01")) or (
        mesh_client.has_tree_prefix(x, "D02")
    )


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
    not_disseases = filter(
        lambda x: not mesh_client.is_disease(x.removeprefix(mesh.owl_iri)), mesh_terms
    )
    ## drop those terms and save result
    pruner = OntologyPruner(mesh)
    pruner.prune(list(not_disseases))
    pruner.save_onto(save_path)


def filter_non_chmical(mesh_path, save_path):
    mesh = Ontology(mesh_path)
    ## keep terms that are outside of the mesh structre to be safe
    mesh_terms = filter(lambda x: x.startswith(mesh.owl_iri), mesh.owl_classes.keys())
    ## filter for terms that are not not chemical

    not_disseases = filter(
        lambda x: not is_chemical(x.removeprefix(mesh.owl_iri)), mesh_terms
    )
    ## drop those terms and save result
    pruner = OntologyPruner(mesh)
    pruner.prune(list(not_disseases))
    pruner.save_onto(save_path)


def filter_non_genetic(mesh_path, save_path):
    mesh = Ontology(mesh_path)
    ## keep terms that are outside of the mesh structre to be safe
    mesh_terms = filter(lambda x: x.startswith(mesh.owl_iri), mesh.owl_classes.keys())
    ## filter for terms that are not genetic
    not_disseases = filter(
        lambda x: not is_genetic(x.removeprefix(mesh.owl_iri)), mesh_terms
    )
    ## drop those terms and save result
    pruner = OntologyPruner(mesh)
    pruner.prune(list(not_disseases))
    pruner.save_onto(save_path)


if __name__ == "__main__":

    target_ontology_train = "doid"
    mesh_path = "resources/mesh.ttl"
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
