from pathlib import Path
import argparse, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.data import paired_files

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); args=ap.parse_args()
    pairs=paired_files(args.root)
    print(f"VALID: {len(pairs)} paired image/mask files")
    for a,b in pairs[:5]: print(a.name,"<->",b.name)

if __name__=="__main__": main()
