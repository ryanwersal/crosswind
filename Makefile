PYVERSION = python3.2
SETUP = ./setup.py
FIND = find

.PHONY: dist install test install-local uninstall-local clean dangerously-clean

dist:
	$(SETUP) build sdist

install-local:
	$(SETUP) install --prefix=$(HOME)/.local

uninstall-local:
	rm -rf $(HOME)/.local/lib/$(PYVERSION)/site-packages/crosswind
	rm -rf $(HOME)/.local/lib/$(PYVERSION)/site-packages/crosswind-*.egg-info
	rm -rf $(HOME)/.local/bin/crosswind

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
	cp -r crosswind crosswind_replace
	$(PYVERSION) ./crosswind --no-diffs -n -j 10 -w crosswind_replace
	rm -rf crosswind
	mv crosswind_replace crosswind
	patch -p0 < python2.patch
	mv crosswind/fixes/imports_fix_alt_formatting.py __TEMPFILE__
	mv crosswind/fixes/fix_imports.py crosswind/fixes/imports_fix_alt_formatting.py
	mv __TEMPFILE__ crosswind/fixes/fix_imports.py
	mv crosswind/fixes/imports2_fix_alt_formatting.py __TEMPFILE__
	mv crosswind/fixes/fix_imports2.py crosswind/fixes/imports2_fix_alt_formatting.py
	mv __TEMPFILE__ crosswind/fixes/fix_imports2.py
	sed -i 's/u"/"/' crosswind/main.py
