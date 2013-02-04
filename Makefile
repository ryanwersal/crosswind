PYVERSION = python3.2
SETUP = ./setup.py
FIND = find

.PHONY: dist install test install-local uninstall-local clean dangerously-clean

dist:
	$(SETUP) build sdist

install-local:
	$(SETUP) install --prefix=$(HOME)/.local

uninstall-local:
	rm -rf $(HOME)/.local/lib/$(PYVERSION)/site-packages/lib3to2
	rm -rf $(HOME)/.local/lib/$(PYVERSION)/site-packages/3to2-*.egg-info
	rm -rf $(HOME)/.local/bin/3to2

install:
	$(SETUP) install

test:
	$(PYVERSION) test_all_fixers.py

clean:
	rm -rf build dist MANIFEST

dangerously-clean: clean
	$(FIND) . \
	\( -name '*~' \
	   -or -name '#*#' \
	   -or -name '*.pyc' \
	   -or -name '*.orig' \
	\) -exec rm -fv {} \;

python2: clean
	cp -r lib3to2 lib3to2_replace
	$(PYVERSION) ./3to2 --no-diffs -n -j 10 -w lib3to2_replace
	rm -rf lib3to2
	mv lib3to2_replace lib3to2
	patch -p0 < python2.patch
	mv lib3to2/fixes/imports_fix_alt_formatting.py __TEMPFILE__
	mv lib3to2/fixes/fix_imports.py lib3to2/fixes/imports_fix_alt_formatting.py
	mv __TEMPFILE__ lib3to2/fixes/fix_imports.py
	mv lib3to2/fixes/imports2_fix_alt_formatting.py __TEMPFILE__
	mv lib3to2/fixes/fix_imports2.py lib3to2/fixes/imports2_fix_alt_formatting.py
	mv __TEMPFILE__ lib3to2/fixes/fix_imports2.py
	sed -i 's/u"/"/' lib3to2/main.py
