import polars as pl
from indra.databases import mesh_client
import obonet
import biomappings
from mapnet.utils import get_current_date_ymd


if __name__ == "__main__":
    g = obonet.read_obo(
        "https://raw.githubusercontent.com/DiseaseOntology/"
        "HumanDiseaseOntology/main/src/ontology/HumanDO.obo"
    )


    known_mappings_path = "knownMaps/doid_to_mesh_provided_maps.tsv"
    predicted_mappings_path = "bertmap/match/repaired_mappings.tsv"

    known_mappings = pl.read_csv(known_mappings_path, separator="\t", infer_schema=False).with_columns(
        pl.col('SrcEntity').str.split('/').list.get(-1).str.replace('_',":").alias('source identifier'), 
        pl.col('TgtEntity').str.split('/').list.get(-1).alias('target identifier')
    )
    predicted_mappings = pl.read_csv(
        predicted_mappings_path, separator="\t", infer_schema=False
    ).with_columns(
        pl.col('SrcEntity').str.split('/').list.get(-1).str.replace('_',":").alias('source identifier'), 
        pl.col('TgtEntity').str.split('/').list.get(-1).alias('target identifier')
    )
    biomappings_maps_doid_to_mesh = (
        pl.from_records(biomappings.load_mappings(), strict=False, infer_schema_length=None)
        .filter(pl.col("source prefix").eq("doid"))
        .filter(pl.col("target prefix").eq("mesh"))
    )
    biomappings_maps_mesh_to_doid = (
        pl.from_records(biomappings.load_mappings(), strict=False, infer_schema_length=None)
        .filter(pl.col("source prefix").eq("mesh"))
        .filter(pl.col("target prefix").eq("doid"))
    )
    biomappings_maps = biomappings_maps_mesh_to_doid.vstack(biomappings_maps_doid_to_mesh)
    res = predicted_mappings.filter(
        (~predicted_mappings["source identifier"].is_in(known_mappings["source identifier"]))
        & (~predicted_mappings["source identifier"].is_in(biomappings_maps["source identifier"]))
        & (~predicted_mappings["target identifier"].is_in(biomappings_maps["target identifier"]))
        & (~predicted_mappings["source identifier"].is_in(biomappings_maps["target identifier"]))
        & (~predicted_mappings["target identifier"].is_in(biomappings_maps["target identifier"]))
        & (~predicted_mappings["target identifier"].is_in(known_mappings["target identifier"]))
    )

    res = res.with_columns(
        pl.lit("DOID").alias('source prefix'),
        pl.col("SrcEntity")
        .str.strip_prefix("http://purl.obolibrary.org/obo/")
        .str.replace("_", ":")
        .map_elements(lambda x: g.nodes[x]["name"], return_dtype=pl.String).alias('source name'),
        pl.lit("skos:exactMatch").alias('relation'),
        pl.lit("MESH").alias('target prefix'),
        pl.col("TgtEntity")
        .str.strip_prefix("http://purl.bioontology.org/ontology/MESH/")
        .map_elements(lambda x: mesh_client.get_mesh_name(x), return_dtype=pl.String).alias("target name"),
        pl.lit("semapv:SemanticSimilarityThresholdMatching").alias('type'), 
        pl.col('Score').alias('confidence'), 
        pl.lit("BERTMap").alias('source'),
        ).select(
            ['source prefix', 'source identifier', 'source name', 'relation', 'target prefix', 'target identifier', 'target name', 'type', 'confidence', 'source']
        ).sort(by=pl.col("source identifier"))



    res.write_csv(
            f"doid_mesh_mappings_bertmap_{get_current_date_ymd()}.tsv", separator="\t"
        )

