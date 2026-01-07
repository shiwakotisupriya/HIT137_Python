'''
Assignment 2 - Question 2
'''


from __future__ import annotations

import os
from glob import glob
from pathlib import Path

import pandas as pd
import numpy as np


# Always resolve paths relative to THIS script location (fixes your error)
BASE_DIR = Path(__file__).resolve().parent

DATA_FOLDER = BASE_DIR / "question2_data"        # creating the folder that contains all the  CSV files
OUTPUT_FOLDER = BASE_DIR / "question2_results"   # saving the result txt files here

STATION_COL = "STATION_NAME"
META_COLS = ["STATION_NAME", "STN_ID", "LAT", "LON"]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

AU_SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"],
}

SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]


# ---------------------------
# Load all the CSV files 
# ---------------------------
def load_all_years(folder_path: Path) -> pd.DataFrame:
    csv_paths = sorted(folder_path.glob("*.csv"))
    if not csv_paths:
        raise FileNotFoundError(
            f"No CSV files found in: {folder_path}\n"
            f"Tip: ensure the folder exists and contains .csv files."
        )

    frames = []
    for p in csv_paths:
        # low_memory=False avoids dtype guessing issues in some CSVs
        frames.append(pd.read_csv(p, low_memory=False))

    combined_df = pd.concat(frames, ignore_index=True)
    return combined_df


def ensure_output_folder(folder_path: Path) -> None:
    folder_path.mkdir(parents=True, exist_ok=True)



# The original data has one column per month (wide format)
# This helper reshapes the data into a long format,
# making it much easier to group, filter, and calculate statistics

def to_long_temperatures(df: pd.DataFrame) -> pd.DataFrame:
    month_cols = [m for m in MONTHS if m in df.columns]
    if not month_cols:
        raise ValueError(
            "Month columns not found. Expected month headers like: "
            + ", ".join(MONTHS)
        )

    id_vars = [c for c in META_COLS if c in df.columns]
    if STATION_COL not in id_vars and STATION_COL in df.columns:
        id_vars.append(STATION_COL)

    long_df = df.melt(
        id_vars=id_vars,
        value_vars=month_cols,
        var_name="month",
        value_name="temp",
    )

    # Ensure numeric and ignore missing/non-numeric values safely
    long_df["temp"] = pd.to_numeric(long_df["temp"], errors="coerce")
    long_df = long_df.dropna(subset=["temp"])

    return long_df


# ---------------------------
# Seasonal averages to Collects temperatures from all stations and years and calculates the average for each season.
# ---------------------------


def compute_seasonal_averages(df: pd.DataFrame) -> dict[str, float]:
    long_df = to_long_temperatures(df)

    month_to_season = {m: s for s, months in AU_SEASONS.items() for m in months}
    long_df["season"] = long_df["month"].map(month_to_season)

    seasonal_avg = (
        long_df.dropna(subset=["season"])
        .groupby("season")["temp"]
        .mean()
        .to_dict()
    )

    return {s: seasonal_avg[s] for s in SEASON_ORDER if s in seasonal_avg}


def save_seasonal_averages(seasonal_avg: dict[str, float], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        for season in SEASON_ORDER:
            if season in seasonal_avg:
                f.write(f"{season}: {seasonal_avg[season]:.1f}°C\n")


# ---------------------------
# Largest Temperature Range:
# Finds the difference between the highest and lowest also temperature recorded at each station
# ---------------------------

def compute_largest_temp_range_stations(df: pd.DataFrame):
    long_df = to_long_temperatures(df)

    if STATION_COL not in long_df.columns:
        raise KeyError(f"Missing required column: {STATION_COL}")

    stats = long_df.groupby(STATION_COL)["temp"].agg(min_temp="min", max_temp="max")
    stats["range"] = stats["max_temp"] - stats["min_temp"]

    max_range = stats["range"].max()
    winners = stats[stats["range"] == max_range].reset_index()

    results = []
    for _, row in winners.iterrows():
        results.append(
            (
                row[STATION_COL],
                {"min": row["min_temp"], "max": row["max_temp"], "range": row["range"]},
            )
        )
    return results


def save_large_temp(winners, out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        for station, d in winners:
            f.write(
                f"Station {station}: Range {d['range']:.1f}°C "
                f"(Max: {d['max']:.1f}°C, Min: {d['min']:.1f}°C)\n"
            )


# ---------------------------
# Temperature Stability:
# Uses standard deviation to identify the most stable and most variable weather stations.
# ---------------------------


def compute_temperature_stability(df: pd.DataFrame):
    long_df = to_long_temperatures(df)

    if STATION_COL not in long_df.columns:
        raise KeyError(f"Missing required column: {STATION_COL}")

    # std with ddof=1 (pandas default). If a station has 1 value, std becomes NaN -> drop it.
    station_std = long_df.groupby(STATION_COL)["temp"].std().dropna()

    min_std = station_std.min()
    max_std = station_std.max()

    most_stable = [(name, val) for name, val in station_std.items() if val == min_std]
    most_variable = [(name, val) for name, val in station_std.items() if val == max_std]

    return most_stable, most_variable


def save_temperature_stability(most_stable, most_variable, out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        for station, std_val in most_stable:
            f.write(f"Most Stable: Station {station}: StdDev {std_val:.1f}°C\n")
        for station, std_val in most_variable:
            f.write(f"Most Variable: Station {station}: StdDev {std_val:.1f}°C\n")


# ---------------------------
# MAIN 
# ---------------------------
def main():
    ensure_output_folder(OUTPUT_FOLDER)

    df_all = load_all_years(DATA_FOLDER)

    # Seasonal Averages
    seasonal_avg = compute_seasonal_averages(df_all)
    save_seasonal_averages(seasonal_avg, OUTPUT_FOLDER / "average_temp.txt")

    # Largest Temperature Range
    winners = compute_largest_temp_range_stations(df_all)
    save_large_temp(winners, OUTPUT_FOLDER / "largest_temp_range_station.txt")

    # Temperature Stability
    most_stable, most_variable = compute_temperature_stability(df_all)
    save_temperature_stability(
        most_stable,
        most_variable,
        OUTPUT_FOLDER / "temperature_stability_stations.txt",
    )

    print("Done! Results saved in:", OUTPUT_FOLDER)


if __name__ == "__main__":
    main()



''' 
Refrences:
Perplexity AI ChatGPT
Prompt used: how can i combine multiple CSV files into a single pandas DataFrame in Python?

ChatGPT: https://chat.openai.com/
Prompt: how can i determine which weather stations have
 the most stable and most variable temperatures using standard deviation in Python
'''