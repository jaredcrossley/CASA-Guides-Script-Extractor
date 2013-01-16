SCRIPTS = benchmark.sh doom.sh report.sh
PYTHON = extractCASAscript.py casa_call.py readcol.py report.py
PARAMS = NGC3256Band3.sh TWHyaBand7.sh AntennaeBand7.sh IRAS16293Band9.sh \
    SgrABand6.sh M100Band3.sh 2011.0.00367.S.sh
DOCS = README
ALLFILES = $(SCRIPTS) $(PYTHON) $(PARAMS) $(DOCS)

all: dist

dist: $(ALLFILES)
	mkdir -p dist
	cp $(ALLFILES) dist/

# Distribute on Mac
dist_mac: dist
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/benchmark.sh    
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/doom.sh
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/report.sh
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/extractCASAscript.py
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/report.py

clean:
	rm -r dist
