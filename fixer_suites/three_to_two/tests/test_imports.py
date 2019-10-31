import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("imports")


def test_various_unchanged(fixer):

    # Enclosed in a string
    s = "'import queue'"
    fixer.unchanged(s)

    # Never was imported
    s = "print(queue)"
    fixer.unchanged(s)


def test_all_nodotted_names_solo(fixer):

    b = "import configparser"
    a = "import ConfigParser"
    fixer.check(b, a)

    b = "from winreg import *"
    a = "from _winreg import *"
    fixer.check(b, a)

    b = "import copyreg"
    a = "import copy_reg"
    fixer.check(b, a)

    b = "import queue"
    a = "import Queue"
    fixer.check(b, a)

    b = "import socketserver"
    a = "import SocketServer"
    fixer.check(b, a)

    b = "import _markupbase"
    a = "import markupbase"
    fixer.check(b, a)

    b = "import builtins"
    a = "import __builtin__"
    fixer.check(b, a)


def test_nodotted_names_duo(fixer):

    b = "import configparser, copyreg"
    a = "import ConfigParser, copy_reg"
    fixer.check(b, a)

    b = "import _markupbase, queue as bob"
    a = "import markupbase, Queue as bob"
    fixer.check(b, a)

    b = "import socketserver, builtins"
    a = "import SocketServer, __builtin__"
    fixer.check(b, a)


def test_nodotted_names_quad(fixer):

    b = "import configparser, winreg, socketserver, _markupbase"
    a = "import ConfigParser, _winreg, SocketServer, markupbase"
    fixer.check(b, a)

    b = "import queue, math, _markupbase, copyreg"
    a = "import Queue, math, markupbase, copy_reg"
    fixer.check(b, a)


def test_all_dotted_names_solo(fixer):

    b = "import dbm.bsd as bsd"
    a = "import dbhash as bsd"
    fixer.check(b, a)

    b = "import dbm.ndbm"
    a = "import dbm"
    fixer.check(b, a)

    b = "import dbm.dumb"
    a = "import dumbdbm"
    fixer.check(b, a)

    b = "from dbm import gnu"
    a = "import gdbm as gnu"
    fixer.check(b, a)

    b = "import html.parser"
    a = "import HTMLParser"
    fixer.check(b, a)

    b = "import html.entities"
    a = "import htmlentitydefs"
    fixer.check(b, a)

    b = "from http import client"
    a = "import httplib as client"
    fixer.check(b, a)

    b = "import http.cookies"
    a = "import Cookie"
    fixer.check(b, a)

    b = "import http.cookiejar"
    a = "import cookielib"
    fixer.check(b, a)

    b = "import tkinter.dialog"
    a = "import Dialog"
    fixer.check(b, a)

    b = "import tkinter._fix"
    a = "import FixTk"
    fixer.check(b, a)

    b = "import tkinter.scrolledtext"
    a = "import ScrolledText"
    fixer.check(b, a)

    b = "import tkinter.tix"
    a = "import Tix"
    fixer.check(b, a)

    b = "import tkinter.constants"
    a = "import Tkconstants"
    fixer.check(b, a)

    b = "import tkinter.dnd"
    a = "import Tkdnd"
    fixer.check(b, a)

    b = "import tkinter.__init__"
    a = "import Tkinter"
    fixer.check(b, a)

    b = "import tkinter"
    a = "import Tkinter"
    fixer.check(b, a)

    b = "import tkinter.colorchooser"
    a = "import tkColorChooser"
    fixer.check(b, a)

    b = "import tkinter.commondialog"
    a = "import tkCommonDialog"
    fixer.check(b, a)

    b = "from tkinter.font import *"
    a = "from tkFont import *"
    fixer.check(b, a)

    b = "import tkinter.messagebox"
    a = "import tkMessageBox"
    fixer.check(b, a)

    b = "import tkinter.turtle"
    a = "import turtle"
    fixer.check(b, a)

    b = "import urllib.robotparser"
    a = "import robotparser"
    fixer.check(b, a)

    b = "import test.support"
    a = "import test.test_support"
    fixer.check(b, a)

    b = "from test import support"
    a = "from test import test_support as support"
    fixer.check(b, a)

    b = "import xmlrpc.client"
    a = "import xmlrpclib"
    fixer.check(b, a)

    b = "from test import support as spam, not_support as not_spam"
    a = "from test import test_support as spam, not_support as not_spam"
    fixer.check(b, a)


def test_dotted_names_duo(fixer):

    b = "import   tkinter.font,  dbm.bsd"
    a = "import   tkFont,  dbhash"
    fixer.check(b, a)

    b = "import test.support,  http.cookies"
    a = "import test.test_support,  Cookie"
    fixer.check(b, a)


def test_from_import(fixer):

    b = "from test.support import things"
    a = "from test.test_support import things"
    fixer.check(b, a)

    b = "from builtins import open"
    a = "from __builtin__ import open"
    fixer.check(b, a)

    b = """from socketserver import (ThreadingUDPServer, DatagramRequestHandler,
                        ThreadingTCPServer, StreamRequestHandler)"""
    a = """from SocketServer import (ThreadingUDPServer, DatagramRequestHandler,
                        ThreadingTCPServer, StreamRequestHandler)"""
    fixer.check(b, a)


def test_dotted_names_quad(fixer):

    b = "import    html.parser as spam,  math,     tkinter.__init__,   dbm.gnu #comment!"
    a = "import    HTMLParser as spam,  math,     Tkinter,   gdbm #comment!"
    fixer.check(b, a)

    b = "import math, tkinter.dnd, dbm.ndbm as one, dbm.ndbm as two, urllib"
    a = "import math, Tkdnd, dbm as one, dbm as two, urllib"
    fixer.check(b, a)


def test_usage(fixer):

    b = """
    import queue as james
    james.do_stuff()"""
    a = """
    import Queue as james
    james.do_stuff()"""
    fixer.check(b, a)

    b = """
    import queue
    queue.do_stuff()"""
    a = """
    import Queue
    Queue.do_stuff()"""
    fixer.check(b, a)

    b = """
    import dbm.gnu
    dbm.gnu.open('generic_file')"""
    a = """
    import gdbm
    gdbm.open('generic_file')"""
    fixer.check(b, a)

    b = """
    import tkinter.dialog, tkinter.colorchooser
    tkinter = tkinter.dialog(tkinter.colorchooser("Just messing around"))
    tkinter.test_should_work = True
    tkinter.dialog.dont.code.like.this = True"""
    a = """
    import Dialog, tkColorChooser
    tkinter = Dialog(tkColorChooser("Just messing around"))
    tkinter.test_should_work = True
    Dialog.dont.code.like.this = True"""
    fixer.check(b, a)

    b = """
    open = bob
    import builtins
    myOpen = builtins.open"""
    a = """
    open = bob
    import __builtin__
    myOpen = __builtin__.open"""
    fixer.check(b, a)


def test_bare_usage(fixer):

    b = """
    import builtins
    hasattr(builtins, "quit")"""
    a = """
    import __builtin__
    hasattr(__builtin__, "quit")"""
    fixer.check(b, a)


def test_no_attribute(fixer):
    b = """
    import collections
    import queue

    MyTuple = collections.namedtuple('MyTuple', ['queue', 'queue1'])

    tuple_instance = MyTuple(queue.Queue(), queue.Queue())

    tuple_instance.queue.put(1)
    tuple_instance.queue1.put(1)"""

    a = """
    import collections
    import Queue

    MyTuple = collections.namedtuple('MyTuple', ['queue', 'queue1'])

    tuple_instance = MyTuple(Queue.Queue(), Queue.Queue())

    tuple_instance.queue.put(1)
    tuple_instance.queue1.put(1)"""
    fixer.check(b, a)
