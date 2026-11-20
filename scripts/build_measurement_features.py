"""Read validated raw PLA attributes without changing the saved spatial analysis."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comet_spatial.measurement_features import build_feature_cache

if __name__=='__main__':
    print(build_feature_cache(ROOT))
