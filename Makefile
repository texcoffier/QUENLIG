V=$(shell python -c "import configuration ; print configuration.version")

help:
	@echo "QUENLIG version $(V)"
	@echo "Makefile Goals:"
	@echo " - plots          : Generate all questions graphs"
	@echo " - regtests       : Run the regression tests"
	@echo " - clean          : Remove not necessary files"
	@echo " - figures        : run 'make' on all 'Questions/*/HTML' dirs"
	@echo " - stats          : Statistics on the source code"
	@echo " - tar            : Make the tar.gz, and verify it"
	@echo " - load_simulator : Run a simulator to see server load"
	@echo "                    It uses real student behavior data"
	@echo " - profiling      : Profil the python functions"
	@echo "                    It uses real student behavior data"
	@echo " - check-questions: Search problems in question definition"
	@echo " - simulator_plot : Compute graphics from simulator data"
	@echo "To run/configure the server, run the command: 'main.py'"

# the following session name must contains the collected student data
# It is necessary to run the load_simulator, profiling and histogram_animation
SESSION=L2unix2010s2
SESSION_STUDENTS=39


# Generate statistic graph
plots:
	for I in `cd Students ; echo *` ; \
		do \
                   if [ -d Students/$$I ] ; \
                        then echo;echo $$I; ./main.py $$I plot >/dev/null ; fi \
	done

regtest:
	Scripts/regtest.py

check-questions:
	@-mkdir Students/check-questions
	# For the cisco questionnary
	echo 4 >Students/check-questions/nr_hosts
	for I in Questions/*/ ; \
        do \
        ./main.py check-questions create $$(echo $$I | sed 's/.$$//') 0 \
                  check-questions --silent ; \
        done

load_simulator: # Use port 34001
	ulimit -s 512 ; \
	TIME_SLICE=300 ; \
	for NR_STUDENTS in 50 100 200 300 400 ; \
	do \
	Scripts/load_simulator.py \
		$$NR_STUDENTS \
		$$TIME_SLICE \
		$(SESSION) \
		1 0 34001 load_simulator \
		 >Stats/load_simulator.$$NR_STUDENTS.$$TIME_SLICE.unix ; \
	done

profiling: # Use port 34002 and 10 requests per student
	ulimit -s 512 ; \
	TIME_SLICE=300 ; \
	Scripts/load_simulator.py \
		$(SESSION_STUDENTS) \
		$$TIME_SLICE \
		$(SESSION) \
		1000 `expr $(SESSION_STUDENTS) '*' 2` 34002 profiling ; \
	awk '/primitive calls/ { T=1 ; } T == 1 { print $$0 ; }' \
		<Students/profiling/logs \
		>Stats/profiling.$(SESSION_STUDENTS)

simulator_plot:
	# Scripts/simulator_plot 0.fixed_ttl
	# Scripts/simulator_plot 1.variable_ttl
	# Scripts/simulator_plot 2.caches_answerable_action
	Scripts/simulator_plot v0.7.variable_ttl

# Compute an animated histogram (very long because it uses the simulator)
# Compute with a time acceleration of 10
# Display histogram every 6 seconds real time (60 seconds simulated time)
xxx.histogram:
	Scripts/load_simulator.py $(SESSION_STUDENTS) 6 $(SESSION) 10 0 6666 xxx histogram
# display the animation
histogram_animation:xxx.histogram
	while true ; do clear ; IFS="" ; while read A ; do case "$$A" in *0*) echo "$$A" ;; *) sleep 0.05 ; clear ;; esac ; done <xxx.histogram ; done


clean:
	@echo "Cleaning"
	@find . -name 'xxx*' -o -name '*~' -o -name '*.pyc' -o -name '#*#' \
		-o -name 'nohup.out' -o -name 'output.ps' -o -name '*.bak' | xargs rm -f
	@-rm -rf Students/profiling Students/regtest
	@for I in Questions/*/HTML ; do ( cd $$I ; if [ -f Makefile ] ; then if grep --silent 'clean:' Makefile ; then echo "Clean $$I" ; $(MAKE) -s clean ; fi ; fi ); done

figures:
	for I in HTML Questions/*/HTML ; do ( cd $$I ; $(MAKE) ) ; done

stat:
	@echo 'Python lines Quenlig : ' `cat *.py Plugins/*/*.py | wc -l`
	@echo 'Python lines Unix    : ' `cat Questions/unix/*.py | wc -l`
	@echo 'Python lines Python  : ' `cat Questions/python/*.py | wc -l`
	@echo 'Python lines Cisco   : ' `cat Questions/cisco*/*.py | wc -l`
	@echo 'CSS lines            : ' `cat HTML/*.css | wc -l`

tags:
	etags $$(find . -name '*.py')

doc:
	cd Documentation ; $(MAKE)

git-commited:
	@if [ "$$(git ls-files -m)" != '' ] ; \
	      then echo 'GIT COMMIT PLEASE' ; exit 1 ; fi

copy-doc:
	cp Documentation/Welcome.html ~/public_html/QUENLIG/doc.html
	cp Documentation/doc.css ~/public_html/QUENLIG/
	cp Documentation/doc.js ~/public_html/QUENLIG/
	cp Documentation/en.html ~/public_html/QUENLIG/
	cp Documentation/plugins.html ~/public_html/QUENLIG/
	cp Documentation/tests.html ~/public_html/QUENLIG/

tar:git-commited regtest clean tags doc copy-doc
	ln -s . QUENLIG-$(V)
	(git ls-files ; \
         echo TAGS ; \
         echo Documentation/plugins.html ; \
         echo Documentation/tests.html ; \
        ) | \
		sed 's/^/QUENLIG-$(V)\//' | \
		grep -v 'HTML/sujet' \
		>xxx.to_be_tarred
	tar -T xxx.to_be_tarred -cvf - | \
		gzip >~/public_html/QUENLIG/QUENLIG-$(V).tar.gz
	rm QUENLIG-$(V) xxx.to_be_tarred
	ls -ls ~/public_html/QUENLIG
	git tag $(V)
	@echo "UPDATE ~/public_html/QUENLIG/Welcome.html"
