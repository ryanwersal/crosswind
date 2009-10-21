PYVERSION = python2.7

install:
	./setup.py install

test: .localtest
	lib3to2/tests/test_all_fixers.py

install-local:
	./setup.py install --prefix=$(HOME)/.local

test-local: install-local
	$(PYVERSION) $(HOME)/.local/lib/$(PYVERSION)/site-packages/lib3to2/tests/test_all_fixers.py

uninstall-local:
	rm -rf $(HOME)/.local/lib/$(PYVERSION)/site-packages/lib3to2
	rm -rf $(HOME)/.local/lib/$(PYVERSION)/site-packages/3to2-*.egg-info
	rm -rf $(HOME)/.local/bin/3to2

clean:
	find . \
	\( -name '*~' \
	   -or -name '#*#' \
	   -or -name '*.pyc' \
	\) -exec rm -fv {} \;
	rm -rfv build dist
