"""Methods for filtering ontologies"""

from indra.databases import mesh_client
from deeponto.onto import Ontology, OntologyPruner


def is_genetic(x: str):
    "Wrapper method for Indra Mesh Client, filtering for genetic classes"
    return mesh_client.has_tree_prefix(x, "G05")


def is_chemical(x: str):
    "Wrapper method for Indra Mesh Client, filtering for chemical classes"
    return (mesh_client.has_tree_prefix(x, "D01")) or (
        mesh_client.has_tree_prefix(x, "D02")
    )


## TODO: Could tie all the bellow methods into method that takes another filter method as argument.


def filter_supplemental(mesh_path: str, save_path: str):
    """Filter supplemental classes out of MESH ontology"""
    mesh = Ontology(mesh_path)
    IRIs = mesh.owl_classes.keys()
    ## remove supplemental IRIs which start with C
    suplementalFilter = lambda x: x.removeprefix(mesh.owl_iri)[0].upper() == "C"
    SuplementalIRIs = filter(suplementalFilter, IRIs)
    pruner = OntologyPruner(mesh)
    pruner.prune(list(SuplementalIRIs))
    pruner.save_onto(save_path)


def filter_non_diseases(mesh_path: str, save_path: str):
    """Filter classes that are not diseases out of MESH ontology"""
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


def filter_non_chemical(mesh_path: str, save_path: str):
    """Filter classes that are not chemicals out of MESH ontology"""
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


def filter_non_genetic(mesh_path: str, save_path: str):
    """Filter classes that are not genetic out of MESH ontology"""
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
