.PHONY: setup datasets datasets-tdd datasets-smoke smoke paper all verify package

setup:
	python -m pip install -r requirements.txt

# Download/generate every supported dataset directly under this repository's data/ directory.
datasets:
	python scripts/download_datasets.py --dataset all

datasets-tdd:
	python scripts/download_datasets.py --dataset tdd

datasets-smoke:
	python scripts/download_datasets.py --dataset smoke

smoke:
	python scripts/run_pipeline.py smoke

paper:
	python scripts/run_pipeline.py paper --download

all:
	python scripts/run_pipeline.py both --download

verify:
	python scripts/acceptance_check.py --output-dir outputs/smoke

package:
	python scripts/package_deliverable.py
