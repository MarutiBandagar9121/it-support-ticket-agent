import kagglehub
import os
import shutil

# Download latest version
path = kagglehub.dataset_download("ahsanneural/synthetic-it-support-tickets")

print("Path to dataset files:", path)
files = os.listdir(path)
print("Files in dataset directory:", files)
os.makedirs("data/raw", exist_ok=True)
# Move files to data directory
shutil.copy(os.path.join(path, files[0]), "data/raw/tickets.csv")