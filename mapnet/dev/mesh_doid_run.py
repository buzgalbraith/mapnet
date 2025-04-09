from deeponto.onto import Ontology
from deeponto.align.bertmap import DEFAULT_CONFIG_FILE, BERTMapPipeline

## setup betmap config
config = BERTMapPipeline.load_bertmap_config(DEFAULT_CONFIG_FILE)
config.known_mappings = "knownMaps/doid_to_mesh_provided_maps.tsv"
config.output_path = "/home/buzgalbraith/workspace/mapnet_new"
config.global_matching.enabled = True

## set up ontologies
src_onto_file = "resources/doid.owl"
tgt_onto_file = "resources/mesh_primary_disease.owl"
src_onto = Ontology(src_onto_file)
tgt_onto = Ontology(tgt_onto_file)

BERTMapPipeline(src_onto, tgt_onto, config)
