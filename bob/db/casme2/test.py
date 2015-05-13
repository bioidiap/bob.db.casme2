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
import bob.db.casme2;

from sqlalchemy import create_engine;
from sqlalchemy.orm import Session, sessionmaker;


protocols = ["fold_{0}".format(str(i)) for i in range(1,27)]
fold_data = {'fold_14': [253, 4], 
             'fold_15': [254, 3], 
             'fold_16': [253, 4], 
             'fold_17': [221, 36], 
             'fold_10': [243, 14], 
             'fold_11': [247, 10], 
             'fold_12': [245, 12], 
             'fold_13': [249, 8], 
             'fold_18': [254, 3], 
             'fold_19': [241, 16], 
             'fold_21': [255, 2], 
             'fold_20': [246, 11], 
             'fold_23': [245, 12], 
             'fold_22': [255, 2], 
             'fold_25': [250, 7], 
             'fold_24': [246, 11], 
             'fold_26': [240, 17], 
             'fold_6': [252, 5], 
             'fold_7': [248, 9], 
             'fold_4': [252, 5], 
             'fold_5': [238, 19], 
             'fold_2': [244, 13], 
             'fold_3': [250, 7], 
             'fold_1': [248, 9], 
             'fold_8': [254, 3], 
             'fold_9': [242, 15]} #For each fold, the correct amount of data for training and testing
             
emotions_data = {'repression': 27, 
                 'sadness': 8, 
                 'disgust': 63, 
                 'others': 99, 
                 'surprise': 25, 
                 'fear': 2, 
                 'happiness': 33}#Number of emotions


client_data = {1: 9, 
               2: 13, 
               3: 7, 
               4: 5, 
               5: 19, 
               6: 5, 
               7: 9, 
               8: 3, 
               9: 15, 
               10: 14, 
               11: 10, 
               12: 12, 
               13: 8, 
               14: 4, 
               15: 3, 
               16: 4, 
               17: 36, 
               18: 3, 
               19: 16, 
               20: 11, 
               21: 2, 
               22: 2, 
               23: 12, 
               24: 11, 
               25: 7, 
               26: 17}                 
             

def db_available(test):
  """Decorator for detecting if OpenCV/Python bindings are available"""
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    dbfile = "./bob/db/casme2/db.sql3"
    if os.path.exists(dbfile):
      return test(*args, **kwargs)
    else:
      raise SkipTest("The database file '%s' is not available; did you forget to run 'bob_dbmanage.py %s create' ?" % (dbfile, 'casme2'))

  return wrapper


@db_available
def test_clients():

  assert True

  # test that the expected number of clients is returned
  db = bob.db.casme2.Database()
  assert len(db.groups()) == 2
  assert len(db.client_ids()) == 26
    
  for c in client_data:
    assert client_data[c] == len(db.objects(protocol='fold_1', model_ids=(c,)))


@db_available
def test_files():
  # test that the files() function returns reasonable numbers of files
  db = bob.db.casme2.Database()
    
  #Checking the amount of data for each fold
  for i in range(len(protocols)):
    assert len(db.objects(protocols[i])) == 257
  
  #Cheking the amount of data fro training and testing for each fold
  for p in protocols:
    train = len(db.objects(protocol=p, groups='train'))
    test = len(db.objects(protocol=p, groups='test'))
    
    assert fold_data[p][0]==train
    assert fold_data[p][1]==test
    

  #Checking the number of emotions
  for e in emotions_data:
    assert emotions_data[e] == len(db.objects(protocol='fold_1', emotions=e))


@db_available
def test_annotations():
  # Tests that for all objects
  db = bob.db.casme2.Database()

  #implement test for annotationsbob/db/casme2/test.py
  for f in db.objects():
      annotations = db.annotations(f)
      assert annotations is not None
      #assert 'actionunit' in annotations



#Check if the client id matches with a substring in the filename ('....sub<ID>...')
def test_subject_id():
  db = bob.db.casme2.Database()

  for f in db.objects():  
    assert f.path.find("sub"+str(f.client_id).zfill(2)) > -1



@db_available
def test_driver_api():

  from bob.db.base.script.dbmanage import main
  assert main('casme2 checkfiles --self-test'.split()) == 0


test_driver_api();
