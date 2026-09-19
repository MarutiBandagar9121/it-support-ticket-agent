from data_utils import load_tickets
from config import settings

PATH = "data/processed/sample_5000.csv"

df = load_tickets(PATH)
print(df.shape)