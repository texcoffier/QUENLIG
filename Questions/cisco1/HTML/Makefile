all:icon-nuage.epsf modes.png sujet

icon-nuage.epsf:icon-nuage.png

%.png:%.svg
	@echo "$*.svg =================> $*.png"
	@inkscape --export-png=xxx-$*.png --without-gui --export-area-drawing \
                 --export-dpi=200 $*.svg
	@convert xxx-$*.png -trim $*.png
	@rm xxx-$*.png

# Les SVG doivent être édité à la main.

sujet:plan1.png plan2.png plan3.png plan4.png

clean:
	-rm -f xxx* *.epsf *.eps plan*.dot plan*.png modes.png modes_small.png


include ../../../Makefile.common
