#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @date:   Wed Jul  4 14:12:51 CEST 2012
#
# @modifying_author: Abdullahi Adamu <research.abdullah@gmail.com>
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

"""Table models and functionality for the CASME2 database adopted from the
"""

import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, or_, and_, not_
from bob.db.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

import xbob.db.verification.utils

import os

Base = declarative_base()


class Client(Base):
    """Information about the clients (identities) of the CASME2 database"""
    __tablename__ = 'client'


    # Group to which the client belongs to
    # NOTES: though this groups have been defined, due to the imbalanced nature of the dataset, its advised to combine all
    # the groups into one, perform dataset imabalance correction and then perform
    #group_choices = ('dev', 'eval', 'world');

    id = Column(Integer, primary_key=True); #The subject ID as in the file
    #sgroup = Column(Enum(*group_choices));
   


    def __init__(self, id):
        self.id = id
        #self.sgroup = sgroup;

    def __repr__(self):
        return "Client<(%d, '%s')>" % (self.id)
        #return "Client<(%d, '%s', '%s')>" % (self.id, self.sgroup)


class File(Base,xbob.db.verification.utils.File ):
    """
    NOTE:this interface is the variant of the CASME2 database which does not use the video files, but rather the ones converted
    into frames of images. (i.e. the ones in the "CROPPED" folder). As such, this folder is supposed to be an abstract
    representation of the video file - in this case, its a fodler containing the video frames.


    This is represent the video file directory containing the frames.
    * the emotions ('happiness', 'repression', 'disgust', 'surprise', 'sadness', 'others') for the client
    * the client id, in this case, each file is a frame in the video
    """
    __tablename__ = 'file'


    # The definitions of the various emotions/expressions from the micro-expression databse in CASME2
    emotion_choices = ('happiness', 'repression', 'disgust', 'surprise',  'sadness', 'fear', 'others');


    ###### COLUMNS #########
    id = Column(Integer, primary_key=True,autoincrement= True);
    #path to the file directory, in this case - its the path to the folder containing the frames
    path = Column(String);  #directory containing the video frames for the CASME2 database
    #client in the file
    client_id = Column(Integer, ForeignKey('client.id'));
    #emotion expressed in the file
    emotion = Column(Enum(*emotion_choices));
    #onset of the emotion
    onset = Column(Integer);
    #apex of the emotion
    apex = Column(Integer);
    #offset of the emotions
    offset = Column(Integer);


    ##### RELATIONSHIPS #####
    # a back-reference from the client class to a list of files
    client = relationship("Client", backref=backref("files", order_by=id))


    def __init__(self, client_id, path, emotion, onset, apex, offset):
        # call base class constructor
        xbob.db.verification.utils.File.__init__(self, client_id = client_id, path = path)

        self.client_id = client_id;
        self.path = path;
        self.emotion = emotion; #emotion
        self.onset =onset; #onset
        self.apex = apex; #apex
        self.offset = offset; #offset

    def __repr__(self):
        return "<File(filename:'%s', Client_id:'%s, emotion:'%s', onset: %d, apex: %d, offset: %d)>" % (
            self.path,self.client_id, self.emotion, self.onset, self.apex, self.offset  );




class Frame(Base, xbob.db.verification.utils.File):
    """
    This is represents the frames in the video file (in this case, contained in the folder)

    It contains the sequence of frames for each file recorded for the subjects in CASME2
    """

    __tablename__ = 'frame'


    id = Column(Integer, primary_key=True, autoincrement= True);
    client_id = Column(Integer, ForeignKey('client.id')); # the client id the fram belongs to
    frame_no = Column('frame_no', Integer); # the frame number
    file_id = Column(Integer,ForeignKey("file.id")); #file id the frame belongs to
    filename = Column(String) # the filename of the jpeg image file - i.e. the frame itself.

    # a back-reference from the client class to a list of files
    files = relationship("File", backref=backref("frames", order_by=frame_no))    


    def __init__(self, path,client_id, file_id,  frame_no, filename):
        # call base class constructor
        xbob.db.verification.utils.File.__init__(self, client_id = client_id, path = path)

        #set the variables
        self.file_id = file_id;
        self.frame_no = frame_no;
        self.filename = filename;

    def __repr__(self):
        #returns representation in string form
        return "Frame<(file_id: %d, frame_no: %d)>" % (self.file_id, self.frame_no);


class ActionUnits(Base):

    __tablename__ = 'actionunits'


    #In this part, we describe the facial action units. There is a prefix attached to the action unit which describes
    # the side of the face which the action unit is activated. For example AU2L, means action unit 2 on the left part of
    # the face,
    # R - Right side of the face
    # L - Left side of the face


    #In addition to that, -1 is used for the apex column of one of the subjects which is supposed to represent an undecided',
    # or unavailable option.


    id = Column(Integer, primary_key= True, autoincrement= True);
    file_id = Column(Integer, ForeignKey('file.id'));
    actionunit = Column(String);

    actionunits = relationship("File", backref=backref("actionunits", order_by=id));

    def __repr__(self):
        return "<ActionUnit(file_id: %d, value: %s)" % (self.file_id, self.actionunit);


class Protocol(Base):
    """The protocols of the CASME2 database."""
    __tablename__ = 'protocol'

    protocol_choices = []
    for i in range(1,27):
        protocol_choices.append("fold_{0}".format(str(i)))

    #id      = Column(Integer, primary_key=True, autoincrement= True)
    name    = Column(Enum(*protocol_choices), primary_key=True)

    def __init__(self, protocol):
        self.name     = protocol

    def __repr__(self):
        return "<Protocol('%s')>" % (
            self.name)


class ClientxProtocol(Base):
    """Cross table between client and protocol."""
    __tablename__ = 'clientXprotocol'

    groups    = ('train','test')
    id          = Column(Integer, primary_key=True, autoincrement= True)
    client_id   = Column(Integer, ForeignKey('client.id')); # the client id the fram belongs to
    protocol_id = Column(String, ForeignKey('protocol.name')); # the protocol id the fram belongs to
    group     = Column(Enum(*groups)) #The purpose of the client

    def __init__(self, client_id, protocol_id, group):
        self.protocol_id = protocol_id
        self.client_id   = client_id
        self.group       = group

    def __repr__(self):
        return "<ClientxProtocol('%s','%s','%s')>" % (
            self.protocol_id, self.client_id, self.group)



