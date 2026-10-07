# Compile any Haskell file into bin/
# to use it...use...
# make bin/valid in the CLI
bin/%: %.hs
	@mkdir -p bin
	ghc $< -outputdir bin -o $@

# Clean a specific compiled program
clean:
	rm -f bin/*.hi bin/*.o

.PHONY: clean