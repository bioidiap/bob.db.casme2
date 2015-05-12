#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @co-author: Abdullah
# @date:   Wed Jul  4 14:12:51 CEST 2012
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module provides the Database interface allowing the user to query the
CASME database.
"""

import os
import six
from .models import *
from .driver import Interface

import xbob.db.verification.utils

SQLITE_FILE = Interface().files()[0]

class Database(xbob.db.verification.utils.SQLiteDatabase):
  """The database class opens and maintains a connection opened to the Database.

  It provides many different ways to probe for the characteristics of the data
  and for the data itself inside the database.
  """

  def __init__(self, original_directory = None, original_extension = '.ppm'):
      #import ipdb; ipdb.set_trace();
  
      # call base class constructor
      xbob.db.verification.utils.SQLiteDatabase.__init__(self, SQLITE_FILE, File, original_directory=original_directory, original_extension=original_extension)
      # defines valid entries for various parameters
      #self.m_groups  = Client.group_choices;
      self.m_protocols = Protocol.protocol_choices;
      self.m_emotions = File.emotion_choices
      self.m_groups = ClientxProtocol.groups      


  def groups(self, protocol=None):
      """Returns the names of all registered groups"""
      return self.m_groups

  def clients(self, protocol=None, groups=None):
      """Returns a list of Client objects for the specific query by the user.

      Keyword Parameters:

      groups
        Ignored

      protocol
        Ignored since clients are identical for all protocols.

      Returns: A list containing all the Client objects which have the desired properties.
      """

      query = self.query(Client)
      return [client for client in query]


  def client_ids(self, groups=None, genders = None, protocol=None):
    """Returns a list of client ids for the specific query by the user.

    Keyword Parameters:

    groups
      One or several groups to which the models belong ('world', 'dev', 'eval').
      If not specified, all groups are returned.

    protocol
      Ignored since clients are identical for all protocols.

    Returns: A list containing all the client ids which have the desired properties.
    """

    return [client.id for client in self.clients(groups, protocol)]


  # model_ids() and client_ids() functions are identical
  model_ids = client_ids


  def get_client_id_from_file_id(self, file_id, **kwargs):
    """Returns the client_id (real client id) attached to the given file_id

    Keyword Parameters:

    file_id
      The file_id to consider

    Returns: The client_id attached to the given file_id
    """
    q = self.query(File).filter(File.id == file_id)

    assert q.count() == 1
    return q.first().client_id


  def get_client_id_from_model_id(self, model_id, **kwargs):
    """Returns the client_id attached to the given model_id

    Keyword Parameters:

    model_id
      The model id to consider

    Returns: The client_id attached to the given model_id
    """
    # client ids and model ids are identical...
    return model_id



  def objects(self, protocol=None, model_ids=None, emotions=None, purposes=None, groups=None):
  #def objects(self, groups=None, protocol=None, model_ids=None, emotions=None, genders = None):  
    """Using the specified restrictions, this function returns a list of File objects.

    Keyword Parameters:

    protocol
      CASME2 protocols.

    model_ids
      If given (as a list of model id's or a single one), only the files belonging to the specified model id is returned.

    emotions
      One or several emotions from - If not specified, objects with all expressions emotions returned.

    purpose
      The purpose of the Object (Train or Test)

    """
    # check that every parameter is as expected
    emotions = self.check_parameters_for_validity(emotions, "emotions", self.m_emotions)
    protocol = self.check_parameters_for_validity(protocol, "protocol", self.m_protocols)[0]
    groups = self.check_parameters_for_validity(groups, "groups", self.m_groups)  
    
    if protocol is None:
      raise ValueError("Keyword ``protocol'' must be defined")

    if type(protocol) is not str:
      raise ValueError("Keyword ``protocol'' must be str")

    #Queruing for protocol
    q      = self.query(File,ClientxProtocol).join(ClientxProtocol, File.client_id==ClientxProtocol.client_id).filter(ClientxProtocol.protocol_id==protocol)
    
    #Querying for emotion
    if emotions:
      q = q.filter(File.emotion.in_(emotions))

    #Querying for models
    if model_ids:
      q = q.filter(File.client_id.in_(model_ids))
      
    #Querying for models
    if groups:
      q = q.filter(ClientxProtocol.group.in_(groups))
      
    
    retval = []
    #post-processing
    for r in list(q):
      r[0].protocol = r[1].protocol_id
      r[0].group = r[1].group
      retval.append(r[0])

    return list(set(retval)) # To remove duplicates   



  def annotations(self, file_id):
    """Returns the annotations for the image with the given file id.

    Keyword Parameters:

    file
      The `File` object to retrieve the annotations for.

    Returns:  the action units for the given file
    """
    self.assert_validity()
    # return the annotations as returned by the call function of the Annotation object
    return file_id.actionunits
