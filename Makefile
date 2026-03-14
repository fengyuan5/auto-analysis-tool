PYTHONPATH ?= src

.PHONY: discover report migration validate test

discover:
	PYTHONPATH=$(PYTHONPATH) python3 -m auto_analysis_tool discover

report:
	PYTHONPATH=$(PYTHONPATH) python3 -m auto_analysis_tool report

migration:
	PYTHONPATH=$(PYTHONPATH) python3 -m auto_analysis_tool migration

validate:
	PYTHONPATH=$(PYTHONPATH) python3 -m auto_analysis_tool validate

test:
	python3 -m unittest discover -s tests
