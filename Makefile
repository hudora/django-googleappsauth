PATH := ./testenv/bin:$(PATH)

default: dependencies check test statistics

check:
	find googleappsauth -name '*.py' | xargs /usr/local/hudorakit/bin/hd_pep8
	/usr/local/hudorakit/bin/hd_pylint -f parseable googleappsauth | tee .pylint.out

install: build
	sudo python setup.py install

dependencies:
	virtualenv testenv
	pip -q install -E testenv -r requirements.txt

statistics:
	sloccount --wide --details googleappsauth | grep -E '^[0-9]' > .sloccount.sc

build:
	python setup.py build sdist bdist_egg

upload: build
	python setup.py sdist upload

clean:
	rm -Rf testenv build dist html test.db .pylint.out .sloccount.sc pip-log.txt
	find . -name '*.pyc' -or -name '*.pyo' -delete

.PHONY: test build clean install upload check
