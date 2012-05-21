PLATFORM = $(shell uname)
ifeq ($(PLATFORM), Darwin)
PYBIN = Python
else
PYBIN = python
endif
PROJ := myriad-worlds
GITHUB_REPO := github.com:oubiwann/$(PROJ).git
LP_REPO := lp:$(PROJ)
AUTHOR ?= oubiwann
MSG_FILE ?= MSG
LIB := myriad


version:
	python $(LIB)/scripts/getVersion.py

keygen:
	@python -c "from myriad import game;from dreamssh.sdk import scripts;scripts.KeyGen()"

run:
	twistd -n myriad

daemon:
	twistd myriad

shell:
	@python -c "from myriad import game;from dreamssh.sdk import scripts;scripts.ConnectToShell()"

stop:
	@python -c "from myriad import game;from dreamssh.sdk import scripts;scripts.StopDaemon()"

run-test:
	make daemon && make shell && make stop

clean:
	find ./ -name "*~" -exec rm {} \;
	find ./ -name "*.pyc" -exec rm {} \;
	find ./ -name "*.pyo" -exec rm {} \;
	find . -name "*.sw[op]" -exec rm {} \;
	rm -rf $(MSG_FILE) $(MSG_FILE).backup _trial_temp/ build/ dist/ MANIFEST \
		CHECK_THIS_BEFORE_UPLOAD.txt *.egg-info

bzr-2-git:
	git init && bzr fast-export `pwd` | git fast-import && git reset HEAD
	git remote add origin git@github.com:oubiwann/$(PROJ).git
	git push -u origin master

msg:
	-@rm $(MSG_FILE)
	@git diff ChangeLog |egrep -v '^\+\+\+'|egrep '^\+.*'|sed -e 's/^+//' >> $(MSG_FILE)
.PHONY: msg

commit: msg
	bzr commit --show-diff --file=$(MSG_FILE)
	@echo '!!! REMOVE THIS LINE !!!' >> $(TMP_FILE)
	@cat $(MSG_FILE) >> $(TMP_FILE)
	@mv $(TMP_FILE) $(MSG_FILE)
	git commit -a -v -t $(MSG_FILE)
	mv $(MSG_FILE) $(MSG_FILE).backup
	touch $(MSG_FILE)

push:
	git push --all git@$(GITHUB_REPO)
	bzr push $(LP_REPO)

push-tags:
	git push --tags git@$(GITHUB_REPO)

push-all: push push-tags
.PHONY: push-all

commit-push: commit push-all
.PHONY: commit-push

stat: msg
	@echo
	@echo "### Changes ###"
	@echo
	-@cat $(MSG_FILE)
	@echo
	@echo "### Git working branch status ###"
	@echo
	@git status -s
	@echo
	@echo "### Git branches ###"
	@echo
	@git branch
	@echo 
	@echo "### Bzr status ###"
	@echo
	@bzr stat
	@echo

status: stat
.PHONY: status

todo:
	git grep -n -i -2 XXX
.PHONY: todo

build:
	@python setup.py build
	@python setup.py sdist

check-dist:
	@echo "Need to fill this in ..."

check: MOD ?= $(LIB)
check: build
	python myriad/testing/runner.py $(MOD)

check-testcase-names:
	@echo "Checking for (possibly) badly named test cases..."
	@find ./$(LIB)|xargs grep Test|grep class|grep -v 'TestCase('

check-integration:
# placeholder for integration tests
.PHONY: check-integration

build-docs:
	cd docs/sphinx; make html

register:
	python setup.py register

upload: check build
	python setup.py sdist upload --show-response

upload-docs: build-docs
	python setup.py upload_docs --upload-dir=docs/html/

virtual-dir-setup: VERSION ?= 2.7
virtual-dir-setup:
	-@test -d .venv-$(VERSION) || virtualenv -p $(PYBIN)$(VERSION) .venv-$(VERSION)
	-@test -e .venv-$(VERSION)/bin/twistd || . .venv-$(VERSION)/bin/activate && pip install twisted
	-@test -e .venv-$(VERSION)/bin/pep8 || . .venv-$(VERSION)/bin/activate && pip install pep8
	-@test -e .venv-$(VERSION)/bin/pyflakes || . .venv-$(VERSION)/bin/activate && pip install pyflakes
	-. .venv-$(VERSION)/bin/activate && pip install lxml
	-. .venv-$(VERSION)/bin/activate && pip install PyOpenSSL
	-. .venv-$(VERSION)/bin/activate && pip install venusian
	-. .venv-$(VERSION)/bin/activate && pip install 'python-dateutil<2.0'
ifeq ($(VERSION), 2.5)
	-. .venv-$(VERSION)/bin/activate && pip install elementtree
	-. .venv-$(VERSION)/bin/activate && pip install simplejson
endif

virtual-builds:
	-@test -e "`which $(PYBIN)2.5`" && VERSION=2.5 make virtual-dir-setup || echo "Couldn't find $(PYBIN)2.5"
	-@test -e "`which $(PYBIN)2.6`" && VERSION=2.6 make virtual-dir-setup || echo "Couldn't find $(PYBIN)2.6"
	-@test -e "`which $(PYBIN)2.7`" && VERSION=2.7 make virtual-dir-setup || echo "Couldn't find $(PYBIN)2.7"

virtual-trial: VERSION ?= 2.7
virtual-trial:
	-. .venv-$(VERSION)/bin/activate && trial ./$(LIB)

virtual-pep8: VERSION ?= 2.7
virtual-pep8:
	-. .venv-$(VERSION)/bin/activate && pep8 --repeat ./$(LIB)

virtual-pyflakes: VERSION ?= 2.7
virtual-pyflakes:
	-. .venv-$(VERSION)/bin/activate && pyflakes ./$(LIB)

virtual-check: VERSION ?= 2.7
virtual-check:
	-VERSION=$(VERSION) make virtual-trial
	-VERSION=$(VERSION) make virtual-pep8
	-VERSION=$(VERSION) make virtual-pyflakes

virtual-setup-build: VERSION ?= 2.7
virtual-setup-build:
	-@. .venv-$(VERSION)/bin/activate && python setup.py build
	-@. .venv-$(VERSION)/bin/activate && python setup.py sdist

virtual-setup-builds: VERSION ?= 2.7
virtual-setup-builds: virtual-builds
	-@test -e "`which python2.5`" && VERSION=2.5 make virtual-setup-build
	-@test -e "`which python2.6`" && VERSION=2.6 make virtual-setup-build
	-@test -e "`which python2.7`" && VERSION=2.7 make virtual-setup-build

virtual-checks: clean virtual-setup-builds
	-@test -e "`which python2.5`" && VERSION=2.5 make virtual-check
	-@test -e "`which python2.6`" && VERSION=2.6 make virtual-check
	-@test -e "`which python2.7`" && VERSION=2.7 make virtual-check
	make check-testcase-names

virtual-uninstall: VERSION ?= 2.7
virtual-uninstall: PACKAGE ?= ""
virtual-uninstall:
	-. .venv-$(VERSION)/bin/activate && pip uninstall $(PACKAGE)

virtual-uninstalls: PACKAGE ?= ""
virtual-uninstalls:
	-@test -e "`which python2.5`" && VERSION=2.5 PACKAGE=$(PACKAGE) make virtual-uninstall
	-@test -e "`which python2.6`" && VERSION=2.6 PACKAGE=$(PACKAGE) make virtual-uninstall
	-@test -e "`which python2.7`" && VERSION=2.7 PACKAGE=$(PACKAGE) make virtual-uninstall

virtual-dir-remove: VERSION ?= 2.7
virtual-dir-remove:
	rm -rfv .venv-$(VERSION)

clean-virtual-builds: clean
	@VERSION=2.5 make virtual-dir-remove
	@VERSION=2.6 make virtual-dir-remove
	@VERSION=2.7 make virtual-dir-remove

virtual-build-clean: clean-virtual-builds build virtual-builds
.PHONY: virtual-build-clean
