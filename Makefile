SCRIPTS = benchmark.sh doom.sh report.sh appendSummary_mac.sh parameters.sh \
    setup.sh
PYTHON = extractCASAscript.py casa_call.py readcol.py report.py
DOCS = README
ALLFILES = $(SCRIPTS) $(PYTHON) $(DOCS)

all: dist

dist: $(ALLFILES)
	mkdir -p dist
	cp $(ALLFILES) dist/

# Distribute on Mac
dist_mac: dist
	sed -i .orig 's~#!/bin/env~#!/usr/bin/env~' dist/benchmark.sh    
	sed -i .orig 's~#!/bin/env~#!/usr/bin/env~' dist/doom.sh
	sed -i .orig 's~#!/bin/env~#!/usr/bin/env~' dist/report.sh
	sed -i .orig 's~#!/bin/env~#!/usr/bin/env~' dist/extractCASAscript.py
	sed -i .orig 's~#!/bin/env~#!/usr/bin/env~' dist/report.py
	sed -i .orig 's~#!/bin/env~#!/usr/bin/env~' dist/appendSummary_mac.sh

clean:
	rm -r dist
