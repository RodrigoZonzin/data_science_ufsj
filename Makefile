all: 
	git add . 
	git commit -m "Commit em $$(date +%Y-%m-%d) by $$(whoami)"
	git push
