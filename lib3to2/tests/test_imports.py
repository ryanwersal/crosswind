from test_all_fixers import lib3to2FixerTestCase

class Test_imports(lib3to2FixerTestCase):
    fixer = "imports"

    def test_various_unchanged(self):
        
        # Enclosed in a string
        s = "'import queue'"
        self.unchanged(s)

        # Never was imported
        s = "print(queue)"
        self.unchanged(s)

        # Never was imported
        s = "gdbm = dbm.gnu"
        self.unchanged(s)

    def test_all_nodotted_names_solo(self):

        b = "import configparser"
        a = "import ConfigParser"
        self.check(b, a)

        b = "from winreg import *"
        a = "from _winreg import *"
        self.check(b, a)

        b = "import copyreg"
        a = "import copy_reg"
        self.check(b, a)

        b = "import queue"
        a = "import Queue"
        self.check(b, a)

        b = "import socketserver"
        a = "import SocketServer"
        self.check(b, a)

        b = "import _markupbase"
        a = "import markupbase"
        self.check(b, a)

    def test_nodotted_names_duo(self):
        
        b = "import configparser, copyreg"
        a = "import ConfigParser, copy_reg"
        self.check(b, a)

        b = "import _markupbase, queue"
        a = "import markupbase, Queue"
        self.check(b, a)

    def test_nodotted_names_quad(self):
        
        b = "import configparser, winreg, socketserver, _markupbase"
        a = "import ConfigParser, _winreg, SocketServer, markupbase"
        self.check(b, a)

        b = "import queue, math, _markupbase, copyreg"
        a = "import Queue, math, markupbase, copy_reg"
        self.check(b, a)
        
    def test_all_dotted_names_solo(self):

        b = "import dbm.bsd"
        a = "import dbhash"
        self.check(b, a)

        b = "import dbm.ndbm"
        a = "import dbm"
        self.check(b, a)

        b = "import dbm.dumb"
        a = "import dumbdbm"
        self.check(b, a)

        b = "import dbm.gnu"
        a = "import gdbm"
        self.check(b, a)

        b = "import html.parser"
        a = "import HTMLParser"
        self.check(b, a)
        
        b = "import html.entities"
        a = "import htmlentitydefs"
        self.check(b, a)

        b = "import http.client"
        a = "import httplib"
        self.check(b, a)

        b = "import http.cookies"
        a = "import Cookie"
        self.check(b, a)

        b = "import http.cookiejar"
        a = "import cookielib"
        self.check(b, a)

        b = "import tkinter.dialog"
        a = "import Dialog"
        self.check(b, a)

        b = "import tkinter._fix"
        a = "import FixTk"
        self.check(b, a)

        b = "import tkinter.scrolledtext"
        a = "import ScrolledText"
        self.check(b, a)

        b = "import tkinter.tix"
        a = "import Tix"
        self.check(b, a)

        b = "import tkinter.constants"
        a = "import Tkconstants"
        self.check(b, a)

        b = "import tkinter.dnd"
        a = "import Tkdnd"
        self.check(b, a)

        b = "import tkinter.__init__"
        a = "import Tkinter"
        self.check(b, a)

        b = "import tkinter.colorchooser"
        a = "import tkColorChooser"
        self.check(b, a)

        b = "import tkinter.commondialog"
        a = "import tkCommonDialog"
        self.check(b, a)

        b = "from tkinter.font import *"
        a = "from tkFont import *"
        self.check(b, a)

        b = "import tkinter.messagebox"
        a = "import tkMessageBox"
        self.check(b, a)

        b = "import tkinter.turtle"
        a = "import turtle"
        self.check(b, a)

        b = "import urllib.robotparser"
        a = "import robotparser"
        self.check(b, a)

        b = "import xmlrpc.client"
        a = "import xmlrpclib"
        self.check(b, a)

    def test_dotted_names_duo(self):
        
        b = "import   tkinter.font,  dbm.bsd"
        a = "import   tkFont,  dbhash"
        self.check(b, a)

        b = "import test.support,  http.cookies"
        a = "import test.test_support,  Cookie"
        self.check(b, a)

    def test_dotted_names_quad(self):
        
        b = "import    html.parser,  math,     tkinter.__init__,   dbm.gnu #comment!"
        a = "import    HTMLParser,  math,     Tkinter,   gdbm #comment!"
        self.check(b, a)
        
        b = "import math, tkinter.dnd, dbm.ndbm, urllib"
        a = "import math, Tkdnd, dbm, urllib"
        self.check(b, a)

    def test_usage(self):
        
        b = """
        import queue
        queue.do_stuff()"""
        a = """
        import Queue
        Queue.do_stuff()"""
        self.check(b, a)

        b = """
        import dbm.gnu
        dbm.gnu.open('generic_file')"""
        a = """
        import gdbm
        gdbm.open('generic_file')"""
        self.check(b, a)
