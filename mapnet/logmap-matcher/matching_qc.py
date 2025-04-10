import polars as pl
from mapnet.utils import format_mappings, quality_check_mappings, get_current_date_ymd
import obonet
from indra.databases import mesh_client


if __name__ == "__main__":

    g = obonet.read_obo(
        "https://raw.githubusercontent.com/DiseaseOntology/"
        "HumanDiseaseOntology/main/src/ontology/HumanDO.obo"
    )
    maps_path = "/home/buzgalbraith/workspace/mapnet/mapnet/logmap-matcher/output/logmap2_mappings.tsv"
    raw_maps = pl.read_csv(
        maps_path,
        separator="\t",
        has_header=False,
        new_columns=["source iri", "target iri", "confidence"],
    )
    formatted_maps = format_mappings(
        df=raw_maps,
        source_prefix="DOID",
        target_prefix="MESH",
        matching_source="LogMap",
        source_name_func=lambda x: g.nodes[x]["name"],
        target_name_func=lambda x: mesh_client.get_mesh_name(x),
    )
    quality_check_mappings(
        formatted_df=formatted_maps,
        target_prefix="MESH",
        source_prefix="DOID",
        known_mappings_path="knownMaps/doid_to_mesh_provided_maps.tsv",
    ).write_csv(
        f"doid_mesh_mappings_logmap_{get_current_date_ymd()}.tsv", separator="\t"
    )
