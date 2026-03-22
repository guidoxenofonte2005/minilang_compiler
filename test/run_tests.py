import os
import subprocess

TEST_DIR = "test/mini_codes"

for file in os.listdir(TEST_DIR):
    if file.endswith(".mini"):
        path = os.path.join(TEST_DIR, file)
        print(f"\n=== Executando {file} ===")
        os.system(f"python src/compiler.py {path}")