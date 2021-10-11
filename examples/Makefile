
export KERNEL?=
KERNEL_OPTS = $(if $(KERNEL),--kernel $(KERNEL),)

UTILS_DIR = ../utils/
PY2JP     = $(UTILS_DIR)py2jp
RUNNB     = python $(UTILS_DIR)runnb.py 

all: tutorial domain focus

.PRECIOUS: tutorial/%.html tutorial/%.ipynb custom_size_domains/%.ipynb custom_size_domains/%.html

tutorial: tutorial/Tutorial.ipynb tutorial/Tutorial.html 
	@echo 
	@echo ">>>>>>>>>>>>>>>>> Tutorial done!"
	@echo 


focus: focus/focus.ipynb focus/focus.html 
	@echo 
	@echo ">>>>>>>>>>>>>>>>> Focus done!"
	@echo 

domain: custom_size_domains/domain.ipynb custom_size_domains/domain.html 
	@echo 
	@echo ">>>>>>>>>>>>>>>>> Custom domains done!"
	@echo 

# tutorial: tutorial/tutorial.html
# 	@echo "> Tutorial done!"


%.html: %.ipynb
	jupyter nbconvert $< --to html
	@echo 
	@echo ">>>>>>>>>>>>>>>>> Created $@ file"
	@echo 

%.ipynb: %.py
	$(PY2JP) $< 
	$(RUNNB) $@ $(KERNEL_OPTS) --run-path .. --inplace 

	@echo 
	@echo ">>>>>>>>>>>>>>>>> Created $@ file"
	@echo 

clean:
	rm -f tutorial/*.ipynb
	rm -f tutorial/*.html

	rm -f custom_size_domains/*.ipynb
	rm -f custom_size_domains/*.html
# 	cd ..;	jupyter nbconvert --execute --inplace --to notebook examples/tutorial/Tutorial.ipynb --ExecutePreprocessor.kernel_name=$(IPYKERNEL_NAME)


