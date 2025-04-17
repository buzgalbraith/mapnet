"""This will fit a Bertmap model to the data and produce mappings between the two ontologies."""

from deeponto.align.bertmap import DEFAULT_CONFIG_FILE
from mapnet.bertmap import load_bertmap


if __name__ == "__main__":
    load_bertmap(
        config=DEFAULT_CONFIG_FILE,
        source_ontology_train="doid",
        target_ontology_train="mesh_primary_disease",
        ontology_paths={
            "mesh_primary_disease": "resources/mesh_primary_disease.owl",
            "doid": "resources/doid.owl",
        },
        known_map_path="knownMaps/doid_to_mesh_provided_maps.tsv",
        train_model=True,
    )
