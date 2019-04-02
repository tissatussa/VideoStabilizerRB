import gi
import io
import os
import subprocess
import sys
import time
import logging
import string
import webbrowser
import re
import signal
import json

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib, Pango
from subprocess import Popen, PIPE, STDOUT, call

gi.require_version('Gst', '1.0')  # GStreamer must be installed : Synaptic OK
from gi.repository import Gst
Gst.init(None)

# NOTE: this is the correct way to do import, but PyCharm gives a FALSE warning:
#       module level import not at top of file
# But PEP is buggy, see https://github.com/PyCQA/pycodestyle/issues/264
# =========================================================================

