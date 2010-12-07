all:plan.png

plan.png:plan.svg
	inkscape --export-png=xxx.png --without-gui --export-area-drawing --export-dpi=150 plan.svg
	convert xxx.png -trim $@


clean:
	-rm xxx* *.epsf plan.*


include ../../../Makefile.common
