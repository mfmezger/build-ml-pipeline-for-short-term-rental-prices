#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    # Drop outliers
    local_path = wandb.use_artifact("sample.csv:latest").file()
    df = pd.read_csv(local_path)
    logger.info("Succes: Read DF from WANDB.")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    logger.info("Succes: Dropped Price Outliers")
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
    args.output_artifact,
    type=args.output_type,
    description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

    logger.info("Succes: Basic Cleaning finished.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="The input artifact that is entered.",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="The output artifact that is created by the script.",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="the type of the output",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="the description of the output.",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="The minimum Price, values lower than that should be dropped.",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="The maximum price, values higher than that should be dropped.",
        required=True
    )


    args = parser.parse_args()

    go(args)