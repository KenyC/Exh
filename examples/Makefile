
export KERNEL?=
KERNEL_OPTS = $(if $(KERNEL),--kernel $(KERNEL),)

UTILS_DIR = ../utils/
PY2JP     = $(UTILS_DIR)py2jp
RUNNB     = python $(UTILS_DIR)runnb.py 

all: tutorial

tutorial: tutorial/Tutorial.html
	@echo 
	@echo ">>>>>>>>>>>>>>>>> Tutorial done!"
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
# 	cd ..;	jupyter nbconvert --execute --inplace --to notebook examples/tutorial/Tutorial.ipynb --ExecutePreprocessor.kernel_name=$(IPYKERNEL_NAME)


