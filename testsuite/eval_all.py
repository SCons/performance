import os
import sys
import sconstest
import sconstest.eval

spec = "default"
if len(sys.argv) > 1:
  spec = sys.argv[1]

print "Converting profiling results..."

# Process all folders
sconstest.eval.eval_all_folders(os.path.join(sconstest.results,spec))

