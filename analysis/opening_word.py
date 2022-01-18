import pandas as pd
import glob

entropy_files = glob.glob("data/opening_word/standardized_entropy/entropy_data_*.csv")

df = pd.concat(
    map(lambda filename: pd.read_csv(filename, header=None), entropy_files),
    ignore_index=True,
)

# Normalize df
words = df[0]
df = df.drop(columns=[0])
df = (df - df.mean()) / df.std()
df.insert(0, 0, words)

df["simple_entropy"] = df[1] + df[2] + df[3] + df[4] + df[5]
df = df.sort_values(by=["simple_entropy"], ascending=[True])
df = df.filter(items=[0, "simple_entropy"])
print(df.head(10))
