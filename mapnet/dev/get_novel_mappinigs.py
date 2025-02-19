import polars as pl
from indra.databases import mesh_client
import obonet
import biomappings
from mapnet.bertmap.utils import get_current_date_ymd

g = obonet.read_obo(
    "https://raw.githubusercontent.com/DiseaseOntology/"
    "HumanDiseaseOntology/main/src/ontology/HumanDO.obo"
)


known_mappings_path = "knownMaps/doid_to_mesh_provided_maps.tsv"
predicted_mappings_path = "bertmap/match/repaired_mappings.tsv"

known_mappings = pl.read_csv(known_mappings_path, separator="\t", infer_schema=False)
predicted_mappings = pl.read_csv(
    predicted_mappings_path, separator="\t", infer_schema=False
)
biomappings_maps_doid_to_mesh = (
    pl.from_records(biomappings.load_mappings(), strict=False, infer_schema_length=None)
    .filter(pl.col("source prefix").eq("doid"))
    .filter(pl.col("target prefix").eq("mesh"))
    .with_columns(
        source_uri="http://purl.obolibrary.org/obo/"
        + pl.col("source identifier").str.replace(":", "_"),
        target_uri="http://purl.bioontology.org/ontology/MESH/"
        + pl.col("target identifier"),
    )
)
biomappings_maps_mesh_to_doid = (
    pl.from_records(biomappings.load_mappings(), strict=False, infer_schema_length=None)
    .filter(pl.col("source prefix").eq("mesh"))
    .filter(pl.col("target prefix").eq("doid"))
    .with_columns(
        source_uri="http://purl.bioontology.org/ontology/MESH/"
        + pl.col("source identifier"),
        target_uri="http://purl.obolibrary.org/obo/"
        + pl.col("target identifier").str.replace(":", "_"),
    )
)
biomappings_maps = biomappings_maps_mesh_to_doid.vstack(biomappings_maps_doid_to_mesh)
res = predicted_mappings.filter(
    (~predicted_mappings["SrcEntity"].is_in(known_mappings["SrcEntity"]))
    & (~predicted_mappings["SrcEntity"].is_in(biomappings_maps["source_uri"]))
    & (~predicted_mappings["TgtEntity"].is_in(biomappings_maps["target_uri"]))
    & (~predicted_mappings["SrcEntity"].is_in(biomappings_maps["target_uri"]))
    & (~predicted_mappings["TgtEntity"].is_in(biomappings_maps["target_uri"]))
)


res.with_columns(
    source_prefix=pl.lit("DOID"),
    source_identifier=pl.col("SrcEntity").str.strip_prefix(
        "http://purl.obolibrary.org/obo/DOID_"
    ),
    source_name=pl.col("SrcEntity")
    .str.strip_prefix("http://purl.obolibrary.org/obo/")
    .str.replace("_", ":")
    .map_elements(lambda x: g.nodes[x]["name"], return_dtype=pl.String),
    relation=pl.lit("skos:exactMatch"),
    target_prefix=pl.lit("MESH"),
    target_identifier=pl.col("TgtEntity").str.strip_prefix(
        "http://purl.bioontology.org/ontology/MESH/"
    ),
    target_name=pl.col("TgtEntity")
    .str.strip_prefix("http://purl.bioontology.org/ontology/MESH/")
    .map_elements(lambda x: mesh_client.get_mesh_name(x), return_dtype=pl.String),
).sort(by=pl.col("source_identifier")).write_csv(
    f"doid_mesh_mappings_bertmap_{get_current_date_ymd()}.tsv", separator="\t"
)
