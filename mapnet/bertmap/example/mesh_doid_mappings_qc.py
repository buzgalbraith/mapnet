"""this will run quality control on the generated matches (ex filtering trivial matchings), and output the results in a format consistent with that used by Biomapping"""

import polars as pl
from indra.databases import mesh_client
import obonet
from mapnet.utils import get_current_date_ymd, get_novel_mappings, format_mappings


def permissive_map(x):
    """a function to get the name of a given DOID entity, will return 'NO NAME FOUND', if the entity does not exist."""
    try:
        return g.nodes[x]["name"]
    except:
        return "NO NAME FOUND"


if __name__ == "__main__":
    g = obonet.read_obo(
        "https://raw.githubusercontent.com/DiseaseOntology/"
        "HumanDiseaseOntology/main/src/ontology/HumanDO.obo"
    )
    known_mappings_path = "knownMaps/doid_to_mesh_provided_maps.tsv"
    predicted_mappings_path = "bertmap/match/repaired_mappings.tsv"
    ## load in predicted mappings and format them
    raw_maps = pl.read_csv(
        predicted_mappings_path,
        separator="\t",
        has_header=True,
    )
    predicted_mappings = format_mappings(
        df=raw_maps,
        source_prefix="DOID",
        target_prefix="MESH",
        matching_source="BERTMAP",
        source_name_func=permissive_map,
        target_name_func=mesh_client.get_mesh_name,
    )

    ## get the novel mappings
    novel_predictions = get_novel_mappings(
        predicted_mappings=predicted_mappings,
        target_prefix="MESH",
        source_prefix="DOID",
        source_name_func=permissive_map,
        target_name_func=mesh_client.get_mesh_name,
        known_mappings_path=known_mappings_path,
    )
    ## write the results to a tsv file.
    novel_predictions.write_csv(
        f"doid_mesh_mappings_bertmap_{get_current_date_ymd()}.tsv", separator="\t"
    )
