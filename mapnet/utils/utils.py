import datetime
import subprocess
import os
from bioregistry.resolve import get_owl_download


def get_current_date_ymd():
    """Returns the current date as a string in YYYY_MM_DD format."""
    now = datetime.datetime.now()
    return now.strftime("%Y_%m_%d")


def download_ontologies(
    target_ontology_train: str,
    source_ontology_train: str,
    source_ontologies_inference: list,
    target_ontologies_inference: list,
    ontologies_path: str,
):
    """Download OWL Files for specified ontologies."""
    os.makedirs(ontologies_path, exist_ok=True)
    ontology_paths = {}
    for ontology in (
        [target_ontology_train, source_ontology_train]
        + source_ontologies_inference
        + target_ontologies_inference
    ):
        if ontology.upper() == "MESH":
            ## bio-registry does not have a download link for mesh so adding this
            ext = ".ttl"
            url = "https://data.bioontology.org/ontologies/MESH/submissions/28/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb"
        else:
            ext = ".owl"
            url = get_owl_download(ontology.upper())
        ontology_path = os.path.join(ontologies_path, ontology.lower() + ext)
        ontology_paths[ontology.lower()] = ontology_path
        if not os.path.isfile(ontology_path):
            print("Downloading {0}".format(ontology))
            cmd = ["wget", "-O", ontology_path, url]
            subprocess.run(cmd)
            ## mesh is large so download the zip and unzip it.
            if ontology.upper() == "MESH":
                cmd_1 = ["mv", ontology_path, ontology_path + ".zip"]
                subprocess.run(cmd_1)
                cmd_2 = ["unzip", ontology_path + ".zip", "-d", ontology_path + "_dir"]
                subprocess.run(cmd_2)
                cmd_3 = ["mv", ontology_path + "_dir/MESH.ttl", ontology_path]
                subprocess.run(cmd_3)
        else:
            print("found {0} at {1}".format(ontology.lower(), ontology_path))
    return ontology_paths
