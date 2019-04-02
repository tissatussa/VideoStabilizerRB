
# Class names should use CamelCase convention
class MyMainWindow(Gtk.Window):
	# Constructor
	def __init__(self):
		Gtk.Window.__init__(self)

		####################################################################
		### WINDOW
		####################################################################

		self.set_property("title", GTXTinfo)
		self.set_property("border-width", 10)

		# center the window horizontally : use CENTER
		# center the window horizontally AND vertically : use CENTER_ALWAYS (!?)
		# >> https://stackoverflow.com/questions/17908584/how-to-set-the-gtk-window-to-the-center-of-screen
		# you must use gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER_ALWAYS) - answered Feb 2 '16 at 2:42
		self.set_property("window_position", Gtk.WindowPosition.CENTER_ALWAYS)

		# print(dir(Gtk.WindowPosition))

		# ['CENTER', 'CENTER_ALWAYS', 'CENTER_ON_PARENT', 'MOUSE', 'NONE', '__abs__', '__add__', '__and__', '__bool__', '__ceil__', '__class__', '__delattr__', '__dict__', '__dir__', '__divmod__', '__doc__', '__enum_values__', '__eq__', '__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__getnewargs__', '__gt__', '__gtype__', '__hash__', '__index__', '__info__', '__init__', '__init_subclass__', '__int__', '__invert__', '__le__', '__lshift__', '__lt__', '__mod__', '__module__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__trunc__', '__xor__', 'bit_length', 'conjugate', 'denominator', 'from_bytes', 'imag', 'numerator', 'real', 'to_bytes', 'value_name', 'value_nick']



		self.set_property("default_width", 800)
		self.set_property("default_height", 500)
		self.set_property("width_request", 800)
		self.set_property("height_request", 500)
		self.set_property("resizable", False)  # only works when w/h request are set
		self.set_icon_from_file(MyFuncs().get_resource_path("icon.png"))

		####################################################################
		### CSS
		####################################################################
		# eg. give a background color to a button ..
		# i discovered and tried many possible solutions, but many failed ..
		# it seems the OS gives a (background) color to buttons
		# and it can hardly be changed ..
		# the only (!?) way to do it : use CSS : see this answer :
		# https://stackoverflow.com/questions/32436862/gtk-widget-cant-change-bg-color-pygtk
		# NOTE: the style can be defined in a seperate file,
		# containing one or more declarations, eg. :
		# .colorize { background: rgba(200,50,50,0.3); }
		# but it can also be defined in a string like this :

		sp = Gtk.CssProvider()  # style_provider

		# RB: you can use load_from_data only once (otherwise overwritten)
		sp.load_from_data(css_data.encode())
		# We use encode() because of this ERROR :
		# TypeError: Item 0: Must be number or single byte string, not str
		# see https://stackoverflow.com/questions/27664937/
		#  gtk-cssprovider-load-from-data-typeerror-item-0-must-be-number-not-str

		GSgd = Gdk.Screen.get_default()
		GSC = Gtk.StyleContext
		GSPPA = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		GSC.add_provider_for_screen(GSgd, sp, GSPPA)

		####################################################################
		# headerBar = Gtk.HeaderBar()
		# headerBar.props.title = "My Title"
		# self.set_titlebar(headerBar)

		# Audio button on right
		# audioButton = Gtk.Button()
		# cdIcon = Gio.ThemedIcon(name="gnome-dev-cdrom-audio")
		# img = Gtk.Image.new_from_gicon(cdIcon, Gtk.IconSize.BUTTON)
		# audioButton.add(img)
		# headerBar.pack_end(audioButton)

		# ====================================================================
		self.myTXTentryFF = Gtk.Entry()  # FFmpeg info line

		# can NOT be set here, nor by CSS ..
		# but we can set padding by CSS !
		# self.myTXTentryFF.set_property("height_request", 36)

		self.myTXTentryFF.set_property("margin-left", 5)
		self.myTXTentryFF.set_property("margin-right", 5)
		self.myTXTentryFF.set_property("can_focus", False)  # otherwise we have some blue border when focussed (click mouse into it)
		self.myTXTentryFF.set_property("editable", False)
		self.myTXTentryFF.get_style_context().add_class("infoLine")

		# ====================================================================
		self.myTXTentryLV = Gtk.Entry()  # Loaded Video info line

		# can NOT be set here, nor by CSS ..
		# but we can set padding by CSS !
		# self.myTXTentryLV.set_property("height_request", 36)

		self.myTXTentryLV.set_property("margin-left", 5)
		self.myTXTentryLV.set_property("margin-right", 5)
		self.myTXTentryLV.set_property("can_focus", False)  # otherwise we have some blue border when focussed (click mouse into it)
		self.myTXTentryLV.set_property("editable", False)
		self.myTXTentryLV.set_property("has_tooltip", True)
		self.myTXTentryLV.get_style_context().add_class("infoLine")

		# ====================================================================
		# >> https://developer.gnome.org/gnome-devel-demos/unstable/textview.py.html.en
		# a scrollbar for the child widget (that is going to be the textview)
		self.myScrolledWindowTrm = Gtk.ScrolledWindow()
		self.myScrolledWindowTrm.set_property("height_request", 150)

		# we scroll only if needed
		self.myScrolledWindowTrm.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

		# ====================================================================
		# a scrollbar for the child widget (that is going to be the textview)
		self.myScrolledWindowLog = Gtk.ScrolledWindow()
		self.myScrolledWindowLog.set_property("height_request", 255)

		# we scroll only if needed
		self.myScrolledWindowLog.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

		# ====================================================================
		# a text buffer (stores text)
		self.myTXTbufferTrm = Gtk.TextBuffer()
		self.myTXTmultiTrm = Gtk.TextView(buffer=self.myTXTbufferTrm)
		self.myTXTmultiTrm.set_property("editable", False)
		# self.myTXTmultiTrm.set_property("cursor_visible", False)

		# NOT possible to set these by CSS !?
		self.myTXTmultiTrm.set_property("margin_left", 5)
		self.myTXTmultiTrm.set_property("margin_right", 5)
		self.myTXTmultiTrm.set_property("margin_top", 10)
		self.myTXTmultiTrm.set_property("margin_bottom", 5)

		self.myTXTmultiTrm.get_style_context().add_class("TXTmultiTrm")
		self.myTXTmultiTrm.get_style_context().add_class("pd5")

		# WORKS ALL
		# self.myTXTmultiTrm.set_property("wrap_mode", True)
		# self.myTXTmultiTrm.set_property("wrap_mode", False)
		# >> wrap_mode False is default
		self.myTXTmultiTrm.set_property("wrap_mode", Gtk.WrapMode.WORD)

		self.myTXTbufferTrm.set_property("text", GtrmTXT)
		self.myScrolledWindowTrm.add(self.myTXTmultiTrm)

		# ====================================================================
		# a text buffer (stores text)
		self.myTXTbufferLog = Gtk.TextBuffer()

		# WORKS
		# self.myTXTmultiLog = Gtk.TextView(buffer=self.myTXTbufferLog)

		# WORKS
		# self.myTXTmultiLog = Gtk.TextView()
		# self.myTXTmultiLog.set_property("buffer", self.myTXTbufferLog)

		# WORKS
		self.myTXTmultiLog = Gtk.TextView()
		self.myTXTmultiLog.set_buffer(self.myTXTbufferLog)

		# self.myTXTmultiLog.modify_cursor(2)  # Expected Gdk.Color, but got int
		# self.myTXTmultiLog.override_cursor(2)  # Expected Gdk.RGBA, but got int

		self.myTXTmultiLog.set_property("editable", False)
		# self.myTXTmultiLog.set_property("cursor_visible", False)

		# NOT possible to set these by CSS !?
		self.myTXTmultiLog.set_property("margin_left", 5)
		self.myTXTmultiLog.set_property("margin_right", 5)
		self.myTXTmultiLog.set_property("margin_top", 0)
		self.myTXTmultiLog.set_property("margin_bottom", 5)

		# ### when using CSS to change the color, text can not be selected
		# ### NOTE: in fact, you CAN select text, but it's not visible ..
		# self.myTXTmultiLog.get_style_context().add_class("[cssname]")

		self.myTXTmultiLog.get_style_context().add_class("TXTmultiLog")
		self.myTXTmultiLog.get_style_context().add_class("pd5")

		# WORKS ALL
		# self.myTXTmultiLog.set_property("wrap_mode", True)
		# self.myTXTmultiLog.set_property("wrap_mode", False)
		# >> wrap_mode False is default
		self.myTXTmultiLog.set_property("wrap_mode", Gtk.WrapMode.WORD)

		self.myTXTbufferLog.set_property("text", GinfoTXT)

		self.myScrolledWindowLog.add(self.myTXTmultiLog)

		# >> does not fully work !? (but DID..)
		# MyFuncs().initTexviewLinks(self.myTXTmultiLog, "testA http://www.imoma.eu testB")

		# ====================================================================
		self.myPRGbar = Gtk.ProgressBar()

		# print(dir(Gtk.ProgressBar.props))

		# ['app_paintable', 'can_default', 'can_focus', 'composite_child', 'double_buffered', 'ellipsize', 'events', 'expand', 'focus_on_click', 'fraction', 'halign', 'has_default', 'has_focus', 'has_tooltip', 'height_request', 'hexpand', 'hexpand_set', 'inverted', 'is_focus', 'margin', 'margin_bottom', 'margin_end', 'margin_left', 'margin_right', 'margin_start', 'margin_top', 'name', 'no_show_all', 'opacity', 'orientation', 'parent', 'pulse_step', 'receives_default', 'scale_factor', 'sensitive', 'show_text', 'style', 'text', 'tooltip_markup', 'tooltip_text', 'valign', 'vexpand', 'vexpand_set', 'visible', 'width_request', 'window']

		self.myPRGbar.set_property("height_request", 40)
		# self.myPRGbar.set_property("width_request", 100)  # does NOT work !?

		# self.myPRGbar.set_property("text", "hallo")
		self.myPRGbar.set_property("show_text", True)

		# NOT possible to set these by CSS !?
		self.myPRGbar.set_property("margin_right", 5)
		self.myPRGbar.set_property("margin_left", 5)
		self.myPRGbar.set_property("margin_top", 10)
		self.myPRGbar.set_property("margin_bottom", 5)

		self.myPRGbar.get_style_context().add_class("bgPRGbar")

		# self.myPRGbar.get_property("valign")
		# self.myPRGbar.set_property("valign", GTK_ALIGN_FILL)

		# does NOT work !?
		# self.myPRGbar.set_justify(Gtk.Justification.LEFT)

		# does NOT work
		# self.myPRGbar.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5, .5, .5, .5))

		# ====================================================================
		# Button INF
		self.myButtonINF = Gtk.Button()
		self.myButtonINF.set_property("label", "video info")
		self.myButtonINF.connect("clicked", BTNclick().fnButtonClickedINF)

		self.myButtonINF.set_property("sensitive", False)

		# ====================================================================
		# Button OPT
		self.myButtonOPT = Gtk.Button()
		self.myButtonOPT.set_property("label", "options")
		self.myButtonOPT.connect("clicked", BTNclick().fnButtonClickedOPT)

		# self.myButtonOPT.set_property("sensitive", False)
		self.myButtonOPT.set_property("sensitive", True)

		# ====================================================================
		# Button BVF
		self.myButtonBVF = Gtk.Button()
		self.myButtonBVF.set_property("label", "browse video")

		# i can NOT put this function into stablize_btnclick.py .. WHY ?
		self.myButtonBVF.connect("clicked", self.fnButtonClickedBVF)

		self.myButtonBVF.set_property("sensitive", False)  # True when ffmpeg binary is found on the user system

		# ====================================================================
		# Button POV
		self.myButtonPOV = Gtk.Button()
		self.myButtonPOV.set_property("label", "play original")
		self.myButtonPOV.connect("clicked", BTNclick().fnButtonClickedPOV)
		self.myButtonPOV.set_property("sensitive", False)  # True after user browsed some video

		# ====================================================================
		# Button STV
		self.myButtonSTV = Gtk.Button()
		self.myButtonSTV.set_property("label", "stabilize")
		self.myButtonSTV.connect("clicked", STVclick().fnButtonClickedSTV)
		self.myButtonSTV.set_property("sensitive", False)  # True after user stabilized some video

		# ====================================================================
		# Button PSV
		self.myButtonPSV = Gtk.Button()
		self.myButtonPSV.set_property("label", "play stabilized")
		self.myButtonPSV.connect("clicked", BTNclick().fnButtonClickedPSV)
		self.myButtonPSV.set_property("sensitive", False)  # True after creation of the stabilized video

		# ====================================================================
		# Button PUV
		self.myButtonPUV = Gtk.Button()
		self.myButtonPUV.set_property("label", "play duo")
		self.myButtonPUV.connect("clicked", BTNclick().fnButtonClickedPUV)
		self.myButtonPUV.set_property("sensitive", False)  # True after creation of the duo video

		# ====================================================================
		# self.myScaleButtonA = Gtk.ScaleButton(Gtk.ICON_SIZE_MENU, float(0), float(2.5), float(0.025), (Gtk.STOCK_ZOOM_FIT, Gtk.STOCK_ZOOM_FIT))
		self.myScaleButtonA = Gtk.ScaleButton("1", float(0), float(2.5), float(0.025), ("3","4"))
		self.myScaleButtonA.set_property("value", float(0.4))

		# ====================================================================
		# 
		self.myHScale = Gtk.HScale()
		self.myHScale.set_range(0, 100)
		# ====================================================================
		# 
		self.mySpinBox = Gtk.Box()
		adj = Gtk.Adjustment(value=50, lower=0, upper=100, step_increment=1, page_increment=5, page_size=0)
		self.mySpinButton = Gtk.SpinButton(adjustment=adj)
		self.mySpinButton.get_style_context().add_class("spinButton")

		# self.mySpinButton.set_property("inner_border", "e")
		self.mySpinButton.set_property("digits", 2)
		self.mySpinButton.set_property("width_request", 200)
		# self.mySpinButton.set_property("height_request", 100)

		# print(dir(self.mySpinButton.props))

		# print(str(type(self.mySpinButton.get_modifier_style())))
		self.mySpinButton.connect("value-changed", BTNclick().fnSpinButtonChanged)
		self.mySpinBox.add(self.mySpinButton)

		# ====================================================================

		# self.myOPTframe = Gtk.Frame(label = '   Saisie   ', margin = 6, height_request = 400)
		self.myOPTframe = Gtk.Frame()
		self.myOPTframe.set_property("label", "    Set Your Options    ")
		self.myOPTframe.set_property("margin", 6)
		self.myOPTframe.set_property("height_request", 395)

		self.myCBduo = Gtk.CheckButton()
		self.myCBduo.set_property("label", "create duo video")
		self.myCBduo.set_property("margin", 6)
		self.myCBduo.connect('toggled', BTNclick().fnCBduoChanged)

		self.myOPTbox = Gtk.Box(orientation=Gtk.Orientation(1))
		self.myOPTbox.pack_start(self.myCBduo, False, False, 0)
		self.myOPTframe.add(self.myOPTbox)

		# ====================================================================
		# a Grid : layout with rows and columns
		self.myGridOptions = Gtk.Grid()
		# print(dir(self.myGrid.props))

		# RB: !? : the content of the grid becomes 100% wide
		self.myGridOptions.set_property("column_homogeneous", True)

		self.myGridOptions.set_property("column_spacing", 6)
		self.myGridOptions.set_property("row_spacing", 2)

		self.myGridOptions.attach(self.myOPTframe, 0, 0, 1, 1)

		# self.myGridOptions.attach(self.myHScale, 0, 0, 1, 1)
		# self.myGridOptions.attach(self.myScaleButtonA, 0, 0, 1, 1)
		# self.myGridOptions.attach(self.mySpinBox, 0, 0, 1, 1)

		# ====================================================================
		# a Grid : layout with rows and columns
		self.myGrid = Gtk.Grid()
		# print(dir(self.myGrid.props))

		# self.myGrid.set_property("width_request", 600)
		# self.myGrid.set_property("height_request", 400)

		# RB: !? : the content of the grid becomes 100% wide
		self.myGrid.set_property("column_homogeneous", True)

		self.myGrid.set_property("column_spacing", 6)
		self.myGrid.set_property("row_spacing", 2)

		# https://stackoverflow.com/questions/11166482/how-to-set-background-color-gtkbox-in-gtk3
		self.myGrid.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.1, .1, .1, .5))

		self.add(self.myGrid)
		self.myGrid.attach(self.myButtonBVF, 0, 0, 1, 1)
		self.myGrid.attach(self.myButtonSTV, 1, 0, 1, 1)
		self.myGrid.attach(self.myButtonPOV, 2, 0, 1, 1)
		self.myGrid.attach(self.myButtonPSV, 3, 0, 1, 1)
		self.myGrid.attach(self.myButtonPUV, 4, 0, 1, 1)
		self.myGrid.attach(self.myButtonINF, 5, 0, 1, 1)
		self.myGrid.attach(self.myButtonOPT, 6, 0, 1, 1)

		self.myGrid.attach(self.myPRGbar, 0, 1, 7, 1)
		self.myGrid.attach(self.myScrolledWindowTrm, 0, 2, 7, 1)
		self.myGrid.attach(self.myScrolledWindowLog, 0, 3, 7, 1)
		self.myGrid.attach(self.myGridOptions, 0, 4, 7, 1)
		self.myGrid.attach(self.myTXTentryFF, 0, 5, 7, 1)
		self.myGrid.attach(self.myTXTentryLV, 0, 6, 7, 1)

		# ====================================================================

		FFline = MyFuncs().rtLineFFinstalled()
		if FFline == "noFFmpeg":
			self.myTXTentryFF.set_property("text", GmyFFnoTXT)
			self.myTXTentryFF.get_style_context().add_class("BGwarn")
		elif FFline == "noVidStab":
			self.myTXTentryFF.set_property("text", GmyFFVSnoTXT)
			self.myTXTentryFF.get_style_context().add_class("BGwarn")
		else:
			self.myTXTentryFF.set_property("text", "using " + FFline)
			MyFuncs().fnSetLVline(self)
			self.myButtonBVF.set_property("sensitive", True)

		# print(str(myWindow.get_property("modal")))
		# myWindow.set_property("modal", True)
		# print(str(type(self)))

	############################################################
	### i can NOT put this function into stablize_btnclick.py ..
	### WHY ?
	############################################################
	# Function : User clicks button BVF
	def fnButtonClickedBVF(self, widget):
		global GmyVideo
		# print("button BVF")
		myBVFdialog = Gtk.FileChooserDialog("Select your video to stabilize", self, Gtk.FileChooserAction.OPEN, ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))
		self.addBVFfilters(myBVFdialog)
		myBVFdialogResponse = myBVFdialog.run()

		if myBVFdialogResponse == Gtk.ResponseType.OK:
			GmyVideo = myBVFdialog.get_filename()
			MyFuncs().fnSetLVline(self)
			tx = "- video file selected -"
			# self.myButtonOPT.set_property("sensitive", True)
		else:
			GmyVideo = ""
			tx = "- NO video file selected -"

			# self.myButtonBVF.set_property("sensitive", True)
			self.myButtonSTV.set_property("sensitive", False)
			self.myButtonPOV.set_property("sensitive", False)
			self.myButtonPSV.set_property("sensitive", False)
			self.myButtonPUV.set_property("sensitive", False)
			self.myButtonINF.set_property("sensitive", False)
			# self.myButtonOPT.set_property("sensitive", False)

			self.myTXTentryLV.set_property("text", svTXT + " : [none]")
			self.myTXTentryLV.set_property("tooltip_text", "")

		self.myTXTbufferTrm.set_property("text", "")
		self.myTXTbufferLog.set_property("text", "")


		self.myPRGbar.set_property("text", tx)
		self.myPRGbar.set_property("fraction", 0)
		myBVFdialog.destroy()


	def addBVFfilters(self, dialog):
		filter_video = Gtk.FileFilter()
		filter_video.set_name("Video files")

		# gathered from several lists ..
		filter_video.add_mime_type("application/x-mpegURL")
		filter_video.add_mime_type("video/3gpp")
		filter_video.add_mime_type("video/avs-video")
		filter_video.add_mime_type("video/dl")
		filter_video.add_mime_type("video/fli")
		filter_video.add_mime_type("video/gl")
		filter_video.add_mime_type("video/mp4")
		filter_video.add_mime_type("video/mpeg")
		filter_video.add_mime_type("video/quicktime")
		filter_video.add_mime_type("video/vdo")
		filter_video.add_mime_type("video/vivo")
		filter_video.add_mime_type("video/vnd.vivo")
		filter_video.add_mime_type("video/vosaic")
		filter_video.add_mime_type("video/webm")
		filter_video.add_mime_type("video/x-dl")
		filter_video.add_mime_type("video/x-dv")
		filter_video.add_mime_type("video/x-fli")
		filter_video.add_mime_type("video/x-flv")
		filter_video.add_mime_type("video/x-gl")
		filter_video.add_mime_type("video/x-m4v")
		filter_video.add_mime_type("video/x-matroska")  # mkv
		filter_video.add_mime_type("video/x-motion-jpeg")
		filter_video.add_mime_type("video/x-mpeg")
		filter_video.add_mime_type("video/x-mpeq2a")
		filter_video.add_mime_type("video/x-ms-asf")
		filter_video.add_mime_type("video/x-ms-wmv")
		filter_video.add_mime_type("video/x-msvideo")
		filter_video.add_mime_type("video/x-qtc")
		filter_video.add_mime_type("video/x-scm")
		filter_video.add_mime_type("video/x-sgi-movie")

		dialog.add_filter(filter_video)

		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)



