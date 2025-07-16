import csv
import os

def split_csv(input_path, output_dir, chunk_size=100):
    os.makedirs(output_dir, exist_ok=True)
    with open(input_path, 'r', encoding='utf-8', newline='') as infile:
        reader = list(csv.reader(infile))
        header = reader[0]
        rows = reader[1:]
        for i in range(0, len(rows), chunk_size):
            chunk = rows[i:i+chunk_size]
            output_path = os.path.join(output_dir, f"chunk_{i//chunk_size+1}.csv")
            with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                writer.writerows(chunk)

if __name__ == "__main__":
    input_csv = "c:/Users/henry/OneDrive/Documents/SkaiTech/skai-scrapping/data/raw/airlines_name_clean.csv"
    output_folder = "c:/Users/henry/OneDrive/Documents/SkaiTech/skai-scrapping/data/raw/split_chunks"
    split_csv(input_csv, output_folder)