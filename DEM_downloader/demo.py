import argparse
import json
import os

from FABDEM import FABDEMDownloader
from Opentopography import OpenTopographyDownloader
from Copernicus import CopernicusDEMDownloader


VALID_SOURCES = ["fabdem", "opentopo-global", "opentopo-usgs", "copernicus"]


def load_task_from_config(config_path, task_name):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    tasks = config.get("tasks", {})
    if task_name not in tasks:
        raise KeyError(f"Task '{task_name}' not found in config file: {config_path}")

    return tasks[task_name], config.get("default_api_key")


def parse_args():
    parser = argparse.ArgumentParser(description="DEM downloader demo")
    parser.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "task_config.json"))
    parser.add_argument("--task", default=None, help="Task name defined in task_config.json")
    parser.add_argument("--source", choices=VALID_SOURCES, default=None)
    parser.add_argument("--south", type=float, default=None)
    parser.add_argument("--north", type=float, default=None)
    parser.add_argument("--west", type=float, default=None)
    parser.add_argument("--east", type=float, default=None)
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--resolution", type=int, default=30, choices=[30, 90])
    return parser.parse_args()


def resolve_args(args):
    if args.task:
        task_config, default_api_key = load_task_from_config(args.config, args.task)
        for field in ["source", "south", "north", "west", "east", "output_dir", "dataset", "resolution"]:
            if getattr(args, field) is None and field in task_config:
                setattr(args, field, task_config[field])

        if args.api_key is None:
            args.api_key = task_config.get("api_key", default_api_key)

    if args.api_key is None:
        args.api_key = "demoapikeyot2022"

    missing = [field for field in ["source", "south", "north", "west", "east"] if getattr(args, field) is None]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Missing required parameters: {joined}. Provide them via CLI or --task.")

    if args.source not in VALID_SOURCES:
        raise ValueError(f"Invalid source: {args.source}")

    return args


def run_demo(args):
    if args.source == "fabdem":
        downloader = FABDEMDownloader(output_dir=args.output_dir)
        downloader.download_fabdem(args.south, args.north, args.west, args.east)
        return

    if args.source == "opentopo-global":
        dataset_name = args.dataset or "COP30"
        downloader = OpenTopographyDownloader(api_key=args.api_key, dem_type="globaldem", output_dir=args.output_dir)
        downloader.download_global_dem(args.south, args.north, args.west, args.east, dataset_name=dataset_name)
        return

    if args.source == "opentopo-usgs":
        dataset_name = args.dataset or "USGS10m"
        downloader = OpenTopographyDownloader(api_key=args.api_key, dem_type="usgsdem", output_dir=args.output_dir)
        downloader.download_usgs_dem(args.south, args.north, args.west, args.east, dataset_name=dataset_name)
        return

    if args.source == "copernicus":
        downloader = CopernicusDEMDownloader(output_dir=args.output_dir, resolution=args.resolution)
        downloader.download_extent(args.west, args.east, args.south, args.north)
        return


if __name__ == "__main__":
    run_demo(resolve_args(parse_args()))
