from mapnet.bertmap.generate_bertmap_predictions import download_ontologies
from mapnet.dev.mesh_filtering import *


if __name__ == "__main__":
    ## download the ontologies. 
    download_ontologies(
        target_ontology_train="mesh",
        source_ontology_train="doid",
        source_ontologies_inference=[],
        target_ontologies_inference=[],
        ontologies_path="resources"
    )
    ## filter the terms 
    mesh_path = 'resources/mesh.ttl'
    primary_path = "resources/mesh_primary.owl"  
    mesh_dissease_path = "resources/mesh_primary_disseae.owl"  
    print("filtering suplemental terms ")
    filter_supplemental(mesh_path=mesh_path, save_path=primary_path)
    print("filtering disseases")
    filter_non_disseases(mesh_path=primary_path, save_path=mesh_dissease_path)