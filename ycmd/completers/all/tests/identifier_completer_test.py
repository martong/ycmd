#!/usr/bin/env python
#
# Copyright (C) 2013  Google Inc.
#
# This file is part of YouCompleteMe.
#
# YouCompleteMe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# YouCompleteMe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YouCompleteMe.  If not, see <http://www.gnu.org/licenses/>.

from nose.tools import eq_
from ycmd.completers.all import identifier_completer as ic
from ycmd.request_wrap import RequestWrap
from ycmd.tests.test_utils import BuildRequest

def BuildRequestWrap( column_num, contents ):
  return RequestWrap( BuildRequest( column_num = column_num,
                                    contents = contents ) )


def GetCursorIdentifier_StartOfLine_test():
  eq_( 'foo', ic._GetCursorIdentifier( BuildRequestWrap( 1, 'foo' ) ) )
  eq_( 'fooBar', ic._GetCursorIdentifier( BuildRequestWrap( 1, 'fooBar' ) ) )


def GetCursorIdentifier_EndOfLine_test():
  eq_( 'foo', ic._GetCursorIdentifier( BuildRequestWrap( 3, 'foo' ) ) )


def GetCursorIdentifier_PastEndOfLine_test():
  eq_( '', ic._GetCursorIdentifier( BuildRequestWrap( 11, 'foo' ) ) )


def GetCursorIdentifier_NegativeColumn_test():
  eq_( 'foo', ic._GetCursorIdentifier( BuildRequestWrap( -10, 'foo' ) ) )


def GetCursorIdentifier_StartOfLine_StopsAtNonIdentifierChar_test():
  eq_( 'foo', ic._GetCursorIdentifier( BuildRequestWrap( 1, 'foo(goo)' ) ) )


def GetCursorIdentifier_AtNonIdentifier_test():
  eq_( 'goo', ic._GetCursorIdentifier( BuildRequestWrap( 4, 'foo(goo)' ) ) )


def GetCursorIdentifier_WalksForwardForIdentifier_test():
  eq_( 'foo', ic._GetCursorIdentifier( BuildRequestWrap( 1, '       foo' ) ) )


def GetCursorIdentifier_FindsNothingForward_test():
  eq_( '', ic._GetCursorIdentifier( BuildRequestWrap( 5, 'foo   ()***()' ) ) )


def GetCursorIdentifier_SingleCharIdentifier_test():
  eq_( 'f', ic._GetCursorIdentifier( BuildRequestWrap( 1, '    f    ' ) ) )


def GetCursorIdentifier_StartsInMiddleOfIdentifier_test():
  eq_( 'foobar', ic._GetCursorIdentifier( BuildRequestWrap( 4, 'foobar' ) ) )


def GetCursorIdentifier_LineEmpty_test():
  eq_( '', ic._GetCursorIdentifier( BuildRequestWrap( 12, '' ) ) )


def PreviousIdentifier_Simple_test():
  eq_( 'foo', ic._PreviousIdentifier( 2, BuildRequestWrap( 4, 'foo' ) ) )


def PreviousIdentifier_WhitespaceAfterIdent_test():
  eq_( 'foo', ic._PreviousIdentifier( 2, BuildRequestWrap( 6, 'foo     ' ) ) )


def PreviousIdentifier_JunkAfterIdent_test():
  eq_( 'foo',
       ic._PreviousIdentifier( 2, BuildRequestWrap( 13, 'foo  ;;()**   ' ) ) )


def PreviousIdentifier_IdentInMiddleOfJunk_test():
  eq_( 'aa',
       ic._PreviousIdentifier( 2, BuildRequestWrap( 13, 'foo  ;;(aa)**   ' ) ) )


def PreviousIdentifier_IdentOnPreviousLine_test():
  eq_( 'aa',
       ic._PreviousIdentifier( 2, BuildRequestWrap( 13, 'foo  ;;(aa)**   ' ) ) )
