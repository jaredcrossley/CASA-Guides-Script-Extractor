all: dist

dist:
	mkdir dist
	cp 2011.0.00367.S.sh AntennaeBand7.sh M100Band3.sh NGC3256Band3.sh \
SgrABand6.sh TWHyaBand7.sh dist/
	cp benchmark.sh doom.sh report.sh dist/
	cp extractCASAscript.py casa_call.py readcol.py report.py dist/
	cp README dist/

# Distribute on Mac
dist_mac: dist
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/benchmark.sh    
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/doom.sh
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/report.sh
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/extractCASAscript.py
	sed --in-place=.orig 's~#!/bin/env~#!/usr/bin/env~' dist/report.py

clean:
	rm -r dist
