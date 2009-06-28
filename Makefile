clean:
	find . \
	\( -name '*~' \
	   -or -name '#*#' \
	   -or -name '*.pyc' \
	\) -exec rm -fv {} \;
