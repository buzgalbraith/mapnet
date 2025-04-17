# Bertmap Matching example
- provided is an example of the Bertmap Matching Pipeline broken into steps. 
- the example is run on the DOID ontology and a subset of MESH containing only primary diseases.
- Please run the scripts in the following order. 
    1. `mesh_doid_setup.py` : This will download the required ontologies, filter Mesh to primary diseases, and find mappings between the two provided in DOID. 
    2. `mesh_doid_run.py` : This will fit a Bertmap model to the data and produce mappings between the two ontologies. 
    3. `mesh_doid_mappings_qc.py` : this will run quality control on the generated matches (ex filtering trivial matchings), and output the results in a format consistent with that used by Biomappings. 
