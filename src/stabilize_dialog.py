
class TRFdialog(Gtk.Dialog):
	# Constructor
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, ".trf file found !", parent, Gtk.DialogFlags.MODAL,
							(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_default_size(250, 100)
		TRFlabel = Gtk.Label("A stabilized video exists !\nOverwrite ?")
		TRFlabel.set_justify(Gtk.Justification.CENTER)
		TRFbox = self.get_content_area()
		TRFbox.add(TRFlabel)
		self.show_all()


# class MSGdialog(Gtk.Dialog):
# 	# Constructor
# 	def __init__(self, parent):
# 		Gtk.Dialog.__init__(self, "system message", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
# 		self.set_default_size(250, 70)
# 		msgLabel = Gtk.Label(myMessage)
# 		msgLabel.set_justify(Gtk.Justification.LEFT)
# 		msgBox = self.get_content_area()
# 		msgBox.add(msgLabel)
# 		self.show_all()
