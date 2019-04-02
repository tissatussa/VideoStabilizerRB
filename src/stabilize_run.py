
myWindow = MyMainWindow()
# print(dir(myWindow.props))
# myWindow.set_property("default_width", 600)
# myWindow.set_property("default_height", 500)
myWindow.connect("delete-event", Gtk.main_quit)
myWindow.show_all()

myWindow.myPRGbar.hide()
myWindow.myGridOptions.hide()


# ?? https://stackoverflow.com/questions/18160315/write-custom-widget-with-gtk3
# myWindow.present()

signal.signal(signal.SIGTERM, MyFuncs().handle_sigterm)
signal.signal(signal.SIGSEGV, MyFuncs().handle_sigsegv)

try:
	Gtk.main()
except KeyboardInterrupt:
	self.clicked_stop()
	# print("keyboard press detected")
	raise
