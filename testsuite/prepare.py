import os
import sconstest

print "Preparing clean installs..."
for p in sconstest.packages.values():
  package_path = p['path']
  if os.path.exists(package_path):
    os.system("rm -rf %s" % package_path)
  archive = p['archive']
  if archive.endswith('.tar'):
    os.system("tar xf %s" % os.path.join('packages', archive))
  else:
    os.system("tar xzf %s" % os.path.join('packages', archive))

