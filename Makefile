
TESTS:=$(wildcard tests/*.py)

test: 
	for f in $(TESTS); do \
		python $$f; \
	done

# test/%.py:
# 	@echo   $@
# 	@python $@