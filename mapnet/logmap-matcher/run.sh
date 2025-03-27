#!/bin/bash 
java -jar \
    --add-opens java.base/java.lang=ALL-UNNAMED \
    /package/logmap/logmap-matcher-4.0.jar \
    MATCHER \
    file:///package/resources/doid.owl \
    file:///package/resources/mesh_primary_disseae.owl \
    file:///package/output/ \
    false ## classify input ontologies along with mapping?



#!/bin/bash 
# java -jar \
    # --add-opens java.base/java.lang=ALL-UNNAMED \
#     logmap-matcher-4.0.jar \
#     MATCHER \
#     file:///Users/f363673/Workspace/gyori_work/logmap-matcher/resources/doid.owl \
#     file:///Users/f363673/Workspace/gyori_work/logmap-matcher/resources/mesh_primary_disseae.owl \
#     file:///Users/f363673/Workspace/gyori_work/logmap-matcher/output/ \
#     false ## classify input ontologies along with mapping?


