all:icon-nuage.epsf modes.png sujet

icon-nuage.epsf:icon-nuage.png

# Les SVG doivent être édité à la main.

sujet:plan1.png plan2.png plan3.png plan4.png

plan0.png:plan0.svg
	inkscape --export-png=xxx.png --without-gui --export-area-drawing --export-dpi=200 $?
	convert xxx.png -trim $@
plan1.png:plan1.svg
	inkscape --export-png=xxx.png --without-gui --export-area-drawing --export-dpi=200 $?
	convert xxx.png -trim $@
plan2.png:plan2.svg
	inkscape --export-png=xxx.png --without-gui --export-area-drawing --export-dpi=200 $?
	convert xxx.png -trim $@
plan3.png:plan3.svg
	inkscape --export-png=xxx.png --without-gui --export-area-drawing --export-dpi=200 $?
	convert xxx.png -trim $@
plan4.png:plan4.svg
	inkscape --export-png=xxx.png --without-gui --export-area-drawing --export-dpi=200 $?
	convert xxx.png -trim $@


clean:
	-rm -f xxx* *.epsf *.eps plan*.dot plan*.png modes.png modes_small.png


include ../../../Makefile.common
