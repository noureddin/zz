all:
	brython-cli --modules
	@echo  # empty line, to separate the prev output
	@ls -sh brython_modules.js

update:
	rm -f brython.min.js brython_stdlib.js
	wget https://cdn.jsdelivr.net/npm/brython@3/brython.min.js \
		 https://cdn.jsdelivr.net/npm/brython@3/brython_stdlib.js

