.SUFFIXES: .png .svg

.svg.png:
	inkscape --export-png=xxx.png $*.svg
	convert -trim xxx.png $*.png
	rm xxx.png

all:good.png very_good.png bad.png very_bad.png
