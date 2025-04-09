"""Methods for filtering ontologies"""
from indra.databases import mesh_client
from deeponto.onto import Ontology, OntologyPruner


save_path = "resources/mesh_disease.owl"


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


def filter_non_diseases(mesh_path, save_path):
    mesh = Ontology(mesh_path)
    ## keep terms that are outside of the mesh structre to be safe
    mesh_terms = filter(lambda x: x.startswith(mesh.owl_iri), mesh.owl_classes.keys())
    ## filter for terms that are not dissaese
    not_diseases = filter(
        lambda x: not mesh_client.is_disease(x.removeprefix(mesh.owl_iri)), mesh_terms
    )
    ## drop those terms and save result
    pruner = OntologyPruner(mesh)
    pruner.prune(list(not_diseases))
    pruner.save_onto(save_path)


def filter_non_chmical(mesh_path, save_path):
    mesh = Ontology(mesh_path)
    ## keep terms that are outside of the mesh structre to be safe
    mesh_terms = filter(lambda x: x.startswith(mesh.owl_iri), mesh.owl_classes.keys())
    ## filter for terms that are not not chemical

    not_diseases = filter(
        lambda x: not is_chemical(x.removeprefix(mesh.owl_iri)), mesh_terms
    )
    ## drop those terms and save result
    pruner = OntologyPruner(mesh)
    pruner.prune(list(not_diseases))
    pruner.save_onto(save_path)


def filter_non_genetic(mesh_path, save_path):
    mesh = Ontology(mesh_path)
    ## keep terms that are outside of the mesh structre to be safe
    mesh_terms = filter(lambda x: x.startswith(mesh.owl_iri), mesh.owl_classes.keys())
    ## filter for terms that are not genetic
    not_diseases = filter(
        lambda x: not is_genetic(x.removeprefix(mesh.owl_iri)), mesh_terms
    )
    ## drop those terms and save result
    pruner = OntologyPruner(mesh)
    pruner.prune(list(not_diseases))
    pruner.save_onto(save_path)
