.. vim: set fileencoding=utf-8 :
.. @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
.. @date:   Thu Dec  6 12:28:25 CET 2012

==============
 User's Guide
==============

This package contains the access API and descriptions for the `CASME2`_ database.
It only contains the Bob_ accessor methods to use the DB directly from python, with our certified protocols.
The actual raw data for the database should be downloaded from the URL provided by the owners of the database upon signing their agreement form.

Our version of the `CASME2`_ database is specifically interfacing the cropped images in the CROPPED folder.
We split the database into several protocols that we have designed ourselves, using some meta-analysis of the dataset.
The identities are split up into three groups:

* the 'world' group for training your algorithm
* the 'dev' group to optimize your algorithm parameters on
* the 'eval' group that should only be used to report results

Additionally, there are different protocols:

* ``'emotion'``: files with different facial expressions are selected



The Database Interface
----------------------

The :py:class:`bob.db.casme2.Database` complies with the standard biometric verification database as described in `bob.db.base <bob.db.base>`, implementing the interface :py:class:`bob.db.base.SQLiteDatabase`.

.. todo::
   Explain the particularities of the :py:class:`bob.db.casme2.Database`.


.. _casme2: http://fu.psych.ac.cn/CASME/casme2-en.php
.. _bob: https://www.idiap.ch/software/bob
