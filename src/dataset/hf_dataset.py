from datasets import load_dataset
import pandas as pd

class HFDateset:
    def __init__(self):
        self.dataset = None
        self.dataset_name = None
        # ds = self.get_hf_dataset(dataset_name)
        # self.set_dataset(ds)

    def get_hf_dataset(self, dataset_name : str):
        try:
            dataset = load_dataset(dataset_name)
            self.dataset_name = dataset_name
            return dataset
        except FileNotFoundError as e:
            print(f"Dataset '{dataset_name}' not found: {e}")
        except ValueError as e:
            print(f"Error loading dataset '{dataset_name}': {e}")
        except Exception as e:
            print(f"Unexpected error loading dataset '{dataset_name}': {e}")
        return None

    def set_dataset(self, dataset):
        df = dataset["train"].to_pandas()
        self.dataset = df

    def get_dataset(self):
        return self.dataset

nane = "Meyerger/ASAG2024"
hf_dataset = HFDateset()
ds = hf_dataset.get_hf_dataset(nane)
hf_dataset.set_dataset(ds)
df = hf_dataset.get_dataset()
# print(len(df))
# print(df.columns)
required_features = ["question",
                     "provided_answer",
                     "reference_answer",
                     "grade",
                     "data_source",
                     "normalized_grade",
                     "weight",
                     "index"]
df_filtered = df.dropna(subset=required_features)
features = df_filtered["data_source"].unique().tolist()
# Removing datasets without the question value removed some of the datasets.
# print(features)

sample_set = []
for feature in features:
    df_sampled = df_filtered.groupby("data_source").head(10)
    sample_set.append(df_sampled)

print(sample_set)