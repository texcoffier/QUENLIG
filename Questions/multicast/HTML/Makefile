all:plan_dot.png plan_neato.png plan_circo.png


plan_dot.png plan_neato.png plan_circo.png:
	inkscape --export-png=xxx.png --without-gui --export-area-drawing --export-dpi=150 $(@:.png=.svg)
	convert xxx.png -trim $@
	rm xxx.png


clean:
	-rm -f plan*

include ../../../Makefile.common
