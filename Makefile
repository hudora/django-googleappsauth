PATH := ./testenv/bin:$(PATH)

default: dependencies check test statistics

check:
	find hudoratools -name '*.py' | xargs /usr/local/hudorakit/bin/hd_pep8
	/usr/local/hudorakit/bin/hd_pylint -f parseable hudoratools | tee pylint.out

install: build
	sudo python setup.py install

test: dependencies
	DJANGO_SETTINGS_MODULE=settings PYTHONPATH=. python hudoratools/templatetags/hudoratools.py
	DJANGO_SETTINGS_MODULE=settings PYTHONPATH=. python hudoratools/forms.py

dependencies:
	virtualenv testenv
	pip -q install -E testenv -r requirements.txt

statistics:
	sloccount --wide --details hudoratools | grep -E '^[0-9]' > sloccount.sc

build:
	python setup.py build sdist bdist_egg

upload: build
	rsync dist/* root@cybernetics.hudora.biz:/usr/local/www/apache22/data/nonpublic/eggs/

clean:
	rm -Rf testenv build dist html test.db hudoratools.egg-info pylint.out sloccount.sc pip-log.txt
	find . -name '*.pyc' -or -name '*.pyo' -delete

.PHONY: test build clean install upload check
