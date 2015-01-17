ci:
	git add *.py Makefile
	git commit
	git push https://github.com/smorad/ast119 master

pull:
	git pull --rebase https://github.com/smorad/ast119 master

