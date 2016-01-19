#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
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

"""This script creates the CASME2 database in a single pass.
"""

import os

from .models import *
import csv;

def add_clients(session, verbose = True):
    """Adds the clients and split up the groups 'world', 'dev', and 'eval'"""

    # Note: This is not the most optimal split of train, validation and the testing set for CASME2,
    if verbose: print('Adding clients to the database ...')
    
    clients = range(1,27)
    for id in clients:
        if verbose>1: print("  Adding client 'm-%03d' to the world set" % id)    
        session.add(Client(id))

    if verbose:print "Commiting changes of clients to db"
    session.commit();



def add_files(session, directory, annotations_file, verbose):
    """
    Adds files with their respective information into the Database
    :param session: DB session
    :param directory: directory to the CASME2 directory containing the folders of subjects.
    :param annotations_file: annotations for the dataset file path
    :param verbose: whether or not to show some information on CLI
    """

    def read_annotation(f):
        """

        :param annotations_file: casme2 information file
        :return: dictionary with containing the files for a certain subject
        """

        if verbose: print (" Reading the annotations file from the directory ...");
        reader = csv.reader(f, delimiter=",", quotechar='\"');

        header = 0;  # header

        annotations = [];

        for i, row in enumerate(reader):
            # read the the action unit set for the particular file (i.e. video frame recording)
            if header != i:
                #read the subjects id
                subject_id = row[0];
                if verbose: print "\nsubject id: %s" % subject_id;

                #read filename
                filename = row[1];
                if verbose: print ("filename: %s" % filename);

                #read onset
                onset = (row[2]);
                if verbose: print("onset: %s" % onset);

                #read apex
                apex = (row[3]);
                if verbose: print("apex: %s" % apex);

                #read offset
                offset = (row[4]);
                if verbose: print("offset: %s" % offset);

                #emotion
                emotion = row[5];
                if verbose: print ("emotion: %s" % emotion);

                #action units
                au_set = row[6];
                if verbose: print ("action units: %s" % au_set);

                #gender
                gender = row[7];
                if verbose: print ("gender: %s" % gender);

                #split the action units by their combination character "+"
                au_split = au_set.split('+');

                annotation_dict = {'subject_id': subject_id, 'filename': filename,
                                   'onset': onset, 'offset': offset, 'apex': apex,
                                   'emotion': emotion, 'au_set': au_split, 'gender': gender};

                annotations.append(annotation_dict);

        return annotations;


    def get_file_annotation(filename, annotationDict, subject_id):
        """

        :param filename:
        :param annotationDict:
        :return: the dicitionary containing information abou the specific file
        """

        for i, annotation_i in enumerate(annotationDict):
            s_id = subject_id.split("sub")[1]
            if annotation_i['filename'] == filename and annotation_i['subject_id'] == str(int(s_id)):

                return annotation_i;
        #nothing was found
        return None;



    # get the annotations file
    if os.path.exists(annotations_file):
        annot_file = open(annotations_file, 'rb');

        if verbose: print("reading annotations file")
        list_annotation = read_annotation(annot_file);
    else:
        print("Sorry, Could not find the annotations file in bob.db.casme2");
        raise "Sorry, there was no annotaitons file found in the directory";
        list_annotation = None;
    if verbose: print("Completed reading annotation files ...")


    #get list of subject directories
    sub_dir = os.listdir(directory);

    for sub_id in sub_dir:
            
        #set the subject id
        subject_id = sub_id;
        if verbose: print("subject_id: %s", subject_id)

        #if(os.path.basename(  directory  ).startswith(".")):
        if(os.path.basename(  os.path.join(directory, sub_id)  ).startswith(".")):
            continue

        #get the directory  for all the subjects video frames
        subject_files_dir = os.listdir(os.path.join(directory, sub_id))

        #make directory to the subjects files
        subject_dir = os.path.join(directory, sub_id);

        #print out verbose
        if verbose: print("reading subject_%s" % sub_id );
        # Get the a specified video file (i.e. folder containing the video frames)

        #loop over files
        for videofile in subject_files_dir:

            videofile_path = os.path.join(subject_dir,videofile);
 
            if(os.path.basename(videofile_path).startswith(".")):
              continue
            
            if verbose: print ("file_path: %s" % videofile_path);

            #Get list of frame files for that video file
            frame_files = os.listdir(os.path.join(subject_dir, videofile));

            #get the file annotation and then save
            annotation = get_file_annotation(videofile, list_annotation, sub_id)

            if annotation != None:

                print ">>annotation",annotation;
                print ">>videopath",str(videofile_path);

                #create and save the file
                file_obj = File(client_id= int(annotation['subject_id']), path= str(videofile_path), emotion=str(annotation['emotion']),
                                onset= int(annotation['onset']),apex= int(annotation['apex']),offset= int(annotation['offset']));

                if verbose: print ">> attaching action_units", annotation['au_set'];
                file_obj.actionunits = [ActionUnits(actionunit = au) for au in annotation['au_set']];

                if verbose: print(">>fileobj created:", file_obj);


                #commit
                session.add(file_obj);
                session.commit();

                #querry to get the file id in the database
                db_file_id = file_obj.id;

                print db_file_id;

            #loop through the frames of the videofile
            for f in frame_files:
                #get the frame id
                img_name, img_ext = f.split('.');
                frame_id = img_name[7:];

                #make the frame path
                frame_path = os.path.join(videofile_path, f );
                if verbose: print("frame_path: %s" % frame_path);

                if verbose: print("frame_id: %s"%frame_id);

                if img_ext == 'jpg':
                    if verbose: print("  Adding file for subject %s - frame %s " % (sub_id, frame_id));

                    frame_obj = Frame(client_id= int(annotation['subject_id']), path = str(f),  frame_no= int(frame_id),
                                      file_id= int(db_file_id), filename= f);

                    session.add(frame_obj);
                    session.commit();

    if verbose: print("Saving annotations, frames and files ...Done!");


def add_protocols(session, verbose):
  """Adds various protocols for the CASME2 database"""
  if verbose: print("Adding protocols ...")
  
  for i in range(1,27):
      protocol_name = "fold_{0}".format(str(i))
      session.add(Protocol(protocol=protocol_name))
  session.commit()



def add_clientxprotocols(session, verbose):
  """ Creating the leave-one-out folds """
  
  if verbose: print("Adding the folds ...")
  
  clients   = range(1,27)
  protocols = range(1,27)
  
  for p in protocols:
    for c in clients:
    
      protocol_name = "fold_{0}".format(p)
    
      if p==c:
        session.add(ClientxProtocol(c, protocol_name, 'test'))
      else:
        session.add(ClientxProtocol(c, protocol_name, 'train'))
  session.commit()



def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2));
  Client.metadata.create_all(engine);
  File.metadata.create_all(engine);
  Frame.metadata.create_all(engine);
  Protocol.metadata.create_all(engine);

# Driver API
# ==========

def create(args):
  """Creates or re-creates this database"""

  from bob.db.base.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2))
  add_clients(s, args.verbose)
  add_files(s, args.directory, args.annotdir, args.verbose)
  add_protocols(s, args.verbose)
  add_clientxprotocols(s, args.verbose)
  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
  parser.add_argument('-v', '--verbose', action='count', help='Do SQL operations in a verbose way?')
  parser.add_argument('-D', '--directory', metavar='DIR', default='../CASME2/Cropped/', help='The path to the directory containing the subjects folders, which have the frames')
  parser.add_argument('--extension', metavar='STR', default='.jpg', help='The file extension of the image files from the CASME2 database')
  parser.add_argument('-A', '--annotdir', metavar='DIR', default='bob/db/casme2/annotations.csv', help="Change the relative path to the directory containing the action_unit information file of the CASME2 database (defaults to %(default)s)")

  parser.set_defaults(func=create) #action
