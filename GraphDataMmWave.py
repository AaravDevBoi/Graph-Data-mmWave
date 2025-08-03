import argparse

import pandas as pd
import ast
import matplotlib.pyplot as plt
import os

class GraphDataMmWave:
    def __init__(self):
        self.input_dir = None
        self.output_dir = None

    def plotAllData(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Prepare plot
        plt.figure(figsize=(14, 7))

        # Process each CSV file
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".csv"):
                file_path = os.path.join(self.input_dir, filename)
                file_id = os.path.splitext(filename)[0]  # Get base filename without extension

                try:
                    df = pd.read_csv(file_path)
                    df["parsed_distances"] = df["distance_data"].apply(lambda x: ast.literal_eval(x)[0])
                    df["ant0"] = df["parsed_distances"].apply(lambda x: x[0])
                    df["ant1"] = df["parsed_distances"].apply(lambda x: x[1])
                    df["ant2"] = df["parsed_distances"].apply(lambda x: x[2])

                    # Plot each antenna with a unique label
                    plt.plot(df["frame_number"], df["ant0"], label=f"{file_id}_ant0", linewidth=1.2)
                    plt.plot(df["frame_number"], df["ant1"], label=f"{file_id}_ant1", linewidth=1.2)
                    plt.plot(df["frame_number"], df["ant2"], label=f"{file_id}_ant2", linewidth=1.2)

                except Exception as e:
                    print(f"⚠️ Error processing {filename}: {e}")

        # Final plot settings
        plt.xlabel("Frame Number")
        plt.ylabel("Distance (meters)")
        plt.title("All Files & Antennas: Distance vs Frame Number")
        plt.legend(fontsize="small", bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
        plt.grid(True)
        plt.tight_layout(rect=[0, 0, 0.98, 1])  # give room for legend

        # Save and show
        output_path = os.path.join(self.output_dir, "all_antennas_all_files_plot.png")
        plt.savefig(output_path)
        print(f"✅ Plot saved to: {output_path}")
        plt.show()

    def plotSpecificCsv(self, csv_file, output_dir):
        # Path to your CSV file
        self.csv_file = csv_file

        # Extract filename only (no folder, no .csv extension)
        csv_basename = os.path.splitext(os.path.basename(self.csv_file))[0]

        # Set up output folder and image name
        self.output_dir = output_dir
        self.output_filename = f"{csv_basename}_distance_plot.png"
        self.output_path = os.path.join(self.output_dir, self.output_filename)

        os.makedirs(self.output_dir, exist_ok=True)

        # Load CSV into DataFrame
        df = pd.read_csv(csv_file)

        # Parse stringified distance data
        df["parsed_distances"] = df["distance_data"].apply(lambda x: ast.literal_eval(x)[0])

        # Extract distances for each antenna
        df["ant0"] = df["parsed_distances"].apply(lambda x: x[0])
        df["ant1"] = df["parsed_distances"].apply(lambda x: x[1])
        df["ant2"] = df["parsed_distances"].apply(lambda x: x[2])

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(df["frame_number"], df["ant0"], label="Antenna 0", linewidth=1.5)
        plt.plot(df["frame_number"], df["ant1"], label="Antenna 1", linewidth=1.5)
        plt.plot(df["frame_number"], df["ant2"], label="Antenna 2", linewidth=1.5)

        plt.xlabel("Frame Number")
        plt.ylabel("Distance (meters)")
        plt.title("Distance vs Frame Number for All Antennas")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save the plot to a PNG file (overwrite if it exists)
        plt.savefig(self.output_path)
        print(f"Plot saved to: {self.output_path}")

        plt.show()


parser = argparse.ArgumentParser(description="A script that accepts command-line arguments.")
parser.add_argument("--graph_all", action="store_true", help="Graph all Data in one Graph, or not")
parser.add_argument("--input_dir", type=str, help="The path to the directory of input files", required=False)
parser.add_argument("--output_dir", type=str, help="The path to the directory of output files", required=False)
parser.add_argument("--csv_file", type=str, help="The path to the csv file containing all data", required=False)
args = parser.parse_args()
plotter = GraphDataMmWave()
print(args.graph_all)
if (args.graph_all == True):
    if (args.input_dir is None or args.output_dir is None):
        parser.error("--input_dir and --output_dir are required.")
    else:
        plotter.plotAllData(args.input_dir, args.output_dir)
else:
    if (args.csv_file is None or args.output_dir is None):
        parser.error("--csv_file and --output_dir are required.")
    else:
        plotter.plotSpecificCsv(args.csv_file, args.output_dir)