from storage.exporter import to_csv
import os

def test_to_csv(tmp_path):
    data = [{'a':1, 'b':2}]
    path = tmp_path / 'out.csv'
    to_csv(data, str(path))
    assert path.exists()