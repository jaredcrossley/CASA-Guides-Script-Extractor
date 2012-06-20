all: dist

dist:
	mkdir dist
	cp 2011.0.00367.S.bash AntennaeBand7.bash M100Band3.bash NGC3256Band3.bash \
SgrABand6.bash TWHyaBand7.bash dist/
	cp benchmark.bash doom.bash report.bash dist/
	cp extractCASAscript.py casa_call.py readcol.py report.py dist/
	cp README dist/

# Distribute on Mac
dist_mac: dist
	sed -i 's\#!/bin/env\#!/usr/bin/env\ ' dist/benchmark.bash    
	sed -i 's\#!/bin/env\#!/usr/bin/env\ ' dist/doom.bash
	sed -i 's\#!/bin/env\#!/usr/bin/env\ ' dist/report.bash
	sed -i 's\#!/bin/env\#!/usr/bin/env\ ' dist/extractCASAscript.py
	sed -i 's\#!/bin/env\#!/usr/bin/env\ ' dist/report.py

clean:
	rm -r dist
