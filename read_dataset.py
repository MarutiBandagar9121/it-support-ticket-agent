import pandas as pd

df = pd.read_csv("data/raw/tickets.csv")
print("shape: ",df.shape)
print("columns: ",df.columns.tolist())
print("types:\n",df.dtypes)
# showing top 5 records
print("head:\n",df.head())
# showing bottom 5 records
print("tail:\n",df.tail())
# showing random 5 records
print("sample:\n",df.sample(5))
# memory usage
df.info(memory_usage="deep")
print(df.isnull().sum())
print(df["status"].value_counts())