import pandas as pd

def to_csv(data: list, path: str):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)