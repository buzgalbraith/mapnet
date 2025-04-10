import polars as pl
import biomappings


def load_biomappings_df(target_prefix: str, source_prefix: str):
    """return a polars data frame with the mappings from biomapping for two given ontologies."""
    forward_df = (
        pl.from_records(
            biomappings.load_mappings(), strict=False, infer_schema_length=None
        )
        .filter(pl.col("source prefix").eq(source_prefix.lower()))
        .filter(pl.col("target prefix").eq(target_prefix.lower()))
    )
    backward_df = (
        pl.from_records(
            biomappings.load_mappings(), strict=False, infer_schema_length=None
        )
        .filter(pl.col("source prefix").eq(target_prefix.lower()))
        .filter(pl.col("target prefix").eq(source_prefix.lower()))
    )
    return forward_df.vstack(backward_df)


def load_known_mappings_df(known_mappings_path: str):
    """return a polars data frame from a tsv with a given set of known mappings"""
    return pl.read_csv(
        known_mappings_path, separator="\t", infer_schema=False
    ).with_columns(
        pl.col("SrcEntity")
        .str.split("/")
        .list.get(-1)
        .str.replace("_", ":")
        .alias("source identifier"),
        pl.col("TgtEntity").str.split("/").list.get(-1).alias("target identifier"),
    )


def quality_check_mappings(
    formatted_df: pl.DataFrame,
    target_prefix: str,
    source_prefix: str,
    known_mappings_path: str = None,
    check_biomappings: bool = True,
    check_known_mappings: bool = True,
):
    """filter out mappings that are already in biomappings and or known mappings from a tsv file"""
    assert (known_mappings_path is not None) or (not check_biomappings)
    if check_biomappings:
        biomappings_maps = load_biomappings_df(
            target_prefix=target_prefix, source_prefix=source_prefix
        )
        formatted_df = formatted_df.filter(
            (
                ~formatted_df["source identifier"].is_in(
                    biomappings_maps["source identifier"]
                )
            )
            & (
                ~formatted_df["target identifier"].is_in(
                    biomappings_maps["target identifier"]
                )
            )
            & (
                ~formatted_df["source identifier"].is_in(
                    biomappings_maps["target identifier"]
                )
            )
            & (
                ~formatted_df["target identifier"].is_in(
                    biomappings_maps["target identifier"]
                )
            )
        )
    if check_known_mappings:
        known_mappings = load_known_mappings_df(known_mappings_path=known_mappings_path)
        formatted_df = formatted_df.filter(
            (
                ~formatted_df["source identifier"].is_in(
                    known_mappings["source identifier"]
                )
            )
            & (
                ~formatted_df["target identifier"].is_in(
                    known_mappings["target identifier"]
                )
            )
        )
    return formatted_df
