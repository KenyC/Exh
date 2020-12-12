# %%
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

# %%
from exh.model.vars import *

vm = VarManager(
	{2: [3, 4], 5: [6, 3]},
	{2: "a",    5: "b"}
)

assert(vm.n      == 30)
assert(vm.memory == [12, 18])
assert(vm.pred_to_vm_index == {2: 0, 5: 1})
assert(vm.offset           == [0, 12])
assert(vm.index(5, (2, 1)) == 3 * 4 + 2 + 6 * 1)




# %%

