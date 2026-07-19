.PHONY: setup smoke paper all verify package
setup:
	python -m pip install -r requirements.txt
smoke:
	python scripts/generate_bootstrap_dataset.py --root data/bootstrap_synthetic --count 48
	python scripts/run_pipeline.py smoke
paper:
	python scripts/run_pipeline.py paper --download
	python scripts/verify_tdd_provenance.py
	python scripts/compare_to_paper.py
	python scripts/acceptance_check.py --output-dir outputs/paper --require-paper-data
all:
	python scripts/run_pipeline.py both --download
verify:
	python scripts/acceptance_check.py --output-dir outputs/smoke
package:
	python scripts/package_deliverable.py
