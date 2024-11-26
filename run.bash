ipython -i \
    -- \
    mapnet/bertmap/generate_bertmap_predictions.py \
    --target_ontology_train DOID \
    --source_ontology_train MESH2024 \
    --config mapnet/bertmap/config/bertmap_config.yaml \
    --train_model