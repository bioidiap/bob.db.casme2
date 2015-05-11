#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
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

"""A few checks at the CASME2 database.
"""

import os, sys
import unittest

from models import *;
import xbob.db.casme2;

from sqlalchemy import create_engine;
from sqlalchemy.orm import Session, sessionmaker;


def db_available(test):
  """Decorator for detecting if OpenCV/Python bindings are available"""
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    dbfile = "./xbob/db/casme2/db.sql3"
    if os.path.exists(dbfile):
      return test(*args, **kwargs)
    else:
      raise SkipTest("The database file '%s' is not available; did you forget to run 'bob_dbmanage.py %s create' ?" % (dbfile, 'casme2'))

  return wrapper


@db_available
def test_clients():
  # test that the expected number of clients is returned
  db = xbob.db.casme2.Database()
  assert len(db.groups()) == 3
  assert len(db.client_ids()) == 26
  assert len(db.client_ids(groups='world')) == 18
  assert len(db.client_ids(groups='dev')) == 4
  assert len(db.client_ids(groups='eval')) == 4
  #assert len(db.client_ids(emotion='surprise')) == 4 #TODO: There is no keyword ``emotion'' for the ``client_ids'' method
  #assert len(db.client_ids(emotion='happiness')) == 2
  #assert len(db.client_ids(emotion='disgust')) == 6


  assert db.model_ids() == [client.id for client in db.clients()]


@db_available
def test_files():
  # test that the files() function returns reasonable numbers of files
  db = xbob.db.casme2.Database()
  assert len(db.objects()) == 257
  #assert len(db.objects(protocol='emotions')) == 26 #TODO: The object method is not using the keyword argument ``protocol''

  # number of world files are identical for all protocols
  #assert len(db.objects(groups='world', protocol='emotion')) == 18 #TODO: The object method is not using the keyword argument ``protocol''
  assert len(db.objects(groups='world')) == 206#186
  assert len(db.objects(groups='dev')) == 33#48
  assert len(db.objects(groups='eval')) == 18#23


@db_available
def test_annotations():
  # Tests that for all objects
  db = xbob.db.casme2.Database()

  #implement test for annotations
  for f in db.objects():
      annotations = db.annotations(f)
      assert annotations is not None
      #assert 'actionunit' in annotations



#Check if the client id matches with a substring in the filename ('....sub<ID>...')
def test_subject_id():
  db = xbob.db.casme2.Database()

  for f in db.objects():  
    assert f.path.find("sub"+str(f.client_id).zfill(2)) > -1



@db_available
def test_driver_api():

  from bob.db.script.dbmanage import main
  assert main('casme2 dumplist --self-test'.split()) == 0
  #assert main('casme2 dumplist --group=dev --protocol=emotions  --emotion=happiness --self-test'.split()) == 2
  assert main('casme2 checkfiles --self-test'.split()) == 0

  #assert main('casme2 reverse ../CASME2/Cropped/sub03/EP08_1 --self-test'.split()) == 29
  #assert main('casme2 path ../CASME2/Cropped/sub03/EP08_1 --self-test'.split()) == 0


test_driver_api();
