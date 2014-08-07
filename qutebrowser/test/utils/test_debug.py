# Copyright 2014 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for qutebrowser.utils.debug."""

import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyle, QFrame

import qutebrowser.utils.debug as debug
from qutebrowser.test.stubs import FakeSignal


class QEnumKeyTests(unittest.TestCase):

    """Tests for qenum_key."""

    def test_no_metaobj(self):
        """Test with an enum with no metaobject."""
        with self.assertRaises(AttributeError):
            # Make sure it doesn't have a meta object
            # pylint: disable=pointless-statement,no-member
            QStyle.PrimitiveElement.staticMetaObject
        key = debug.qenum_key(QStyle, QStyle.PE_PanelButtonCommand)
        self.assertEqual(key, 'PE_PanelButtonCommand')

    def test_metaobj(self):
        """Test with an enum with metaobject."""
        # pylint: disable=pointless-statement
        QFrame.staticMetaObject  # make sure it has a metaobject
        key = debug.qenum_key(QFrame, QFrame.Sunken)
        self.assertEqual(key, 'Sunken')

    def test_add_base(self):
        """Test with add_base=True."""
        key = debug.qenum_key(QFrame, QFrame.Sunken, add_base=True)
        self.assertEqual(key, 'QFrame.Sunken')

    def test_int_noklass(self):
        """Test passing an int without explicit klass given."""
        with self.assertRaises(TypeError):
            debug.qenum_key(QFrame, 42)

    def test_int(self):
        """Test passing an int with explicit klass given."""
        key = debug.qenum_key(QFrame, 0x0030, klass=QFrame.Shadow)
        self.assertEqual(key, 'Sunken')

    def test_unknown(self):
        """Test passing an unknown value."""
        key = debug.qenum_key(QFrame, 0x1337, klass=QFrame.Shadow)
        self.assertEqual(key, '0x1337')

    def test_reconverted(self):
        """Test passing a flag value which was re-converted to an enum."""
        # FIXME maybe this should return the right thing anyways?
        debug.qenum_key(Qt, Qt.Alignment(int(Qt.AlignLeft)))

class TestDebug(unittest.TestCase):

    """Test signal debug output functions."""

    def setUp(self):
        self.signal = FakeSignal()

    def test_signal_name(self):
        """Test signal_name()."""
        self.assertEqual(debug.signal_name(self.signal), 'fake')

    def test_dbg_signal(self):
        """Test dbg_signal()."""
        self.assertEqual(debug.dbg_signal(self.signal, [23, 42]),
                         'fake(23, 42)')

    def test_dbg_signal_eliding(self):
        """Test eliding in dbg_signal()."""
        self.assertEqual(debug.dbg_signal(self.signal,
                                          [12345678901234567890123]),
                         'fake(1234567890123456789\u2026)')

    def test_dbg_signal_newline(self):
        """Test dbg_signal() with a newline."""
        self.assertEqual(debug.dbg_signal(self.signal, ['foo\nbar']),
                         'fake(foo bar)')


if __name__ == '__main__':
    unittest.main()
