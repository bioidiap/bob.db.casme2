#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Sun 15 Apr 14:01:39 2012 
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Prints the version of bob and exits
"""

def main():
  """Main routine, called by the script that gets the version of bob"""

  import pkg_resources
  packages = pkg_resources.require('bob')
  this = packages[0]
  deps = packages[1:]

  print("The installed version of %s is %s" % (this.key, this.version))
  print("%s is installed at: %s" % (this.key, this.location)
  print("%s depends on the following Python packages:" % (this.key,))
  for d in deps:
    print(" * %s: %s (%s)" % (d.key, d.version, d.location))

  return 0
