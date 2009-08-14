default:
	./setup.py build
    
install: default
	./setup.py install

test:
	lib3to2/tests/test_all_fixers.py

clean:
	find . \
	\( -name '*~' \
	   -or -name '#*#' \
	   -or -name '*.pyc' \
	\) -exec rm -fv {} \;
