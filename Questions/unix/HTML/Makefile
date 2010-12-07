include ../../../Makefile.common

figures:boxes.png graphe.ps graphe.png tree.png graphe_cercle.pdf graphe_cercle.eps

graphe_cercle.pdf graphe_cercle.eps: graphe_cercle.png
	convert graphe_cercle.png $@

graphe_cercle.png: graphe.dot

clean:
	-rm tree.png tree_small.png graphe_cercle.eps graphe_cercle.pdf graphe_cercle.png graphe_cercle_small.png graphe_small.png graphe.png graphe.ps


