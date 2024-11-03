#!/usr/bin/env python
"""
Download from W&B the raw dataset, apply basic data cleaning, and export the result to a new artifact.
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(
        job_type="basic_cleaning", project="nyc_airbnb", group="basic_cleaning"
    )
    run.config.update(args)

    # Download the artifact from W&B
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    # Dropping duplicates
    logger.info("Dropping duplicates")
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Dropping rows with missing values
    logger.info("Dropping rows with missing values")
    df = df.dropna()

    # Dropping outliers
    logger.info("Dropping outliers")
    df = df[(df["price"] >= args.min_price) & (df["price"] <= args.max_price)]

    # Convert last_review to datetime
    logger.info("Converting last_review to datetime")
    df["last_review"] = pd.to_datetime(df["last_review"])

    # Drop rows not in a proper geolocation
    logger.info("Dropping rows with improper geolocation")
    df = df[
        (df["latitude"].between(40.5, 41.2)) & (df["longitude"].between(-74.25, -73.50))
    ]

    # Save the cleaned dataset to a new artifact
    logger.info("Saving cleaned dataset to a new artifact")
    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact, type=args.output_type, description=args.output_description
    )

    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A step for basic data cleaning")

    parser.add_argument(
        "--input_artifact", type=str, help="Input artifact to be cleaned", required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Output artifact after cleaning",
        required=True,
    )

    parser.add_argument(
        "--output_type", type=str, help="Type of the output artifact", required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the output artifact",
        required=True,
    )

    parser.add_argument(
        "--min_price", type=float, help="Minimum price to consider", required=True
    )

    parser.add_argument(
        "--max_price", type=float, help="Maximum price to consider", required=True
    )

    args = parser.parse_args()

    go(args)
