from pathlib import Path

print(Path.cwd())

file_name = Path("id.txt")

file_path = Path.cwd() / "data" / file_name

print(file_path)
