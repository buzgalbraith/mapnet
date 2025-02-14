import polars as pl
from indra.databases import mesh_client 
import obonet
g = obonet.read_obo(
    "https://raw.githubusercontent.com/DiseaseOntology/"
    "HumanDiseaseOntology/main/src/ontology/HumanDO.obo"
)


known_mappings_path = 'knownMaps/doid_to_mesh_provided_maps.tsv'
predicted_mappings_path = 'bertmap/match/repaired_mappings.tsv'

known_mappings = pl.read_csv(known_mappings_path, separator='\t', infer_schema=False)
predicted_mappings = pl.read_csv(predicted_mappings_path, separator='\t', infer_schema=False)

res = predicted_mappings.filter(~predicted_mappings["SrcEntity"].is_in(known_mappings["SrcEntity"]))


res.with_columns(
    source_prefix = pl.lit("DOID"), 
    source_identifier = pl.col('SrcEntity').str.strip_prefix('http://purl.obolibrary.org/obo/DOID_'), 
    source_name = pl.col('SrcEntity').str.strip_prefix('http://purl.obolibrary.org/obo/').str.replace("_",":").map_elements(lambda x: g.nodes[x]["name"], return_dtype=pl.String),
    relation = pl.lit('skos:exactMatch'), 
    target_prefix = pl.lit("MESH"), 
    target_identifier = pl.col('TgtEntity').str.strip_prefix('http://purl.bioontology.org/ontology/MESH/'), 
    target_name = pl.col('TgtEntity').str.strip_prefix('http://purl.bioontology.org/ontology/MESH/').map_elements(lambda x: mesh_client.get_mesh_name(x), return_dtype=pl.String),
)