import polars as pl
import biomappings
from typing import Callable


def load_biomappings_df(target_prefix: str, source_prefix: str):
    """return a polars data frame with the mappings from biomapping for two given ontologies."""
    forward_df = (
        pl.from_records(
            biomappings.load_mappings(), strict=False, infer_schema_length=None
        )
        .filter(pl.col("source prefix").eq(source_prefix.lower()))
        .filter(pl.col("target prefix").eq(target_prefix.lower()))
    ).select(
        [
            "source identifier",
            "source name",
            "target identifier",
            "target name",
        ]
    )
    ## want to check if there are any mappings going in the other direction, and if so rename the columns to keep them consistent
    backward_df = (
        pl.from_records(
            biomappings.load_mappings(), strict=False, infer_schema_length=None
        )
        .filter(pl.col("source prefix").eq(target_prefix.lower()))
        .filter(pl.col("target prefix").eq(source_prefix.lower()))
        .rename(
            {
                "source identifier": "target identifier",
                "source name": "target name",
                "target identifier": "source identifier",
                "target name": "source name",
            }
        )
        .select(
            [
                "source identifier",
                "source name",
                "target identifier",
                "target name",
            ]
        )
    )
    return forward_df.vstack(backward_df)


def load_known_mappings_df(
    known_mappings_path: str, source_name_func: Callable, target_name_func: Callable
):
    """return a polars data frame from a tsv with a given set of known mappings"""
    return (
        pl.read_csv(known_mappings_path, separator="\t", infer_schema=False)
        .with_columns(
            pl.col("SrcEntity")
            .str.split("/")
            .list.get(-1)
            .str.replace("_", ":")
            .alias("source identifier"),
            pl.col("TgtEntity").str.split("/").list.get(-1).alias("target identifier"),
        )
        .with_columns(
            pl.col("source identifier")
            .map_elements(source_name_func, return_dtype=pl.String)
            .alias("source name"),
            pl.col("target identifier")
            .map_elements(target_name_func, return_dtype=pl.String)
            .alias("target name"),
        )
        .select(
            [
                "source identifier",
                "source name",
                "target identifier",
                "target name",
            ]
        )
    )


def get_novel_mappings(
    predicted_mappings: pl.DataFrame,
    target_prefix: str,
    source_prefix: str,
    source_name_func: Callable,
    target_name_func: Callable,
    known_mappings_path: str = None,
    check_biomappings: bool = True,
    check_known_mappings: bool = True,
):
    """filter out mappings that are already in biomappings and or known mappings from a tsv file"""
    assert (known_mappings_path is not None) or (not check_biomappings)

    ## load in evidence
    evidence = None
    if check_biomappings:
        evidence = load_biomappings_df(
            target_prefix=target_prefix, source_prefix=source_prefix
        )
    if check_known_mappings:
        known_mappings = load_known_mappings_df(
            known_mappings_path=known_mappings_path,
            source_name_func=source_name_func,
            target_name_func=target_name_func,
        )
        evidence = (
            known_mappings if (evidence is None) else evidence.vstack(known_mappings)
        )
    ## find classes that had mappings in the predictions and no mappings in the evidence
    novel_predictions = predicted_mappings.join(
        evidence, on=["target identifier"], how="anti"
    )
    novel_predictions = novel_predictions.join(
        evidence, on=["source identifier"], how="anti"
    ).sort(by=pl.col("source identifier"))
    return novel_predictions
