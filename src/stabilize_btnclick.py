
class BTNclick(object):

	def fnSpinButtonChanged(self, widget):
		print("button SpinButton changed")
		# # rint(str(type(widget)))
		# # print(dir(widget))
		print(widget.get_value())
		# pass

	def fnCBduoChanged(self, widget):
		# print("CBduo changed * "+str(widget.get_active()))
		# # rint(str(type(widget)))
		# # print(dir(widget))
		pass

	# Function : User clicks button INF
	def fnButtonClickedINF(self, widget):
		# print("button INF")

		myWindow.myGridOptions.hide()
		myWindow.myPRGbar.hide()
		myWindow.myScrolledWindowLog.hide()

		myWindow.myTXTmultiTrm.set_property("margin_top", 10)
		myWindow.myScrolledWindowTrm.set_property("height_request", 407)
		myWindow.myScrolledWindowTrm.show()
		myWindow.myTXTbufferTrm.set_property("text", MyFuncs().rtVideoMeta())

		myWindow.myButtonINF.set_property("sensitive", False)
		# myWindow.myButtonOPT.set_property("sensitive", (GmyVideo != ""))

	# Function : User clicks button OPT
	def fnButtonClickedOPT(self, widget):
		# print("button OPT")

		myWindow.myPRGbar.hide()
		myWindow.myScrolledWindowLog.hide()
		myWindow.myScrolledWindowTrm.hide()
		myWindow.myGridOptions.show()

		# myWindow.myButtonINF.set_property("sensitive", True)
		# myWindow.myButtonOPT.set_property("sensitive", False)

	# Function : User clicks button Play Original Video
	def fnButtonClickedPOV(self, widget):
		# print("button POV")

		statusPSV = myWindow.myButtonPSV.get_property("sensitive")
		statusPUV = myWindow.myButtonPSV.get_property("sensitive")
		statusINF = myWindow.myButtonINF.get_property("sensitive")
		# statusOPT = myWindow.myButtonOPT.get_property("sensitive")

		def fnGO():
			def fnEND():
				myWindow.myButtonBVF.set_property("sensitive", True)
				myWindow.myButtonSTV.set_property("sensitive", True)
				myWindow.myButtonPOV.set_property("sensitive", True)
				myWindow.myButtonPSV.set_property("sensitive", statusPSV)
				myWindow.myButtonPUV.set_property("sensitive", statusPUV)
				myWindow.myButtonINF.set_property("sensitive", statusINF)
				# myWindow.myButtonOPT.set_property("sensitive", statusOPT)

			# the -autoexit flag causes ffplay to exit and return a status code when the audio file is done playing.
			# args = ['ffplay', '-x', '320', '-y', '180', "-autoexit", '-i', GmyVideo]

			args = []
			args.append('./ffplay_here')
			args.append('-v')
			args.append('quiet')  # -v error : this 'loglevel' gives no header info !
			args.append('-hide_banner')

			# 0: infinite
			# args.append('-loop')
			# args.append('0')

			args.append('-x')
			args.append(GPXPLAYW)
			args.append('-y')
			args.append(GPXPLAYH)
			args.append('-i')
			args.append(GmyVideo)


			# subprocess.Popen(args)
			# p = subprocess.Popen(args)
			# p.wait()
			# Popen(args)  # Popen works also without subprocess
			subprocess.call(args)
			# call(args)  # call works also without subprocess

			# cmd = "ffplay \"" + GmyVideo + "\"" +"\n"
			# length = len(cmd)
			# self.terminal.feed_child(cmd, length)

			# ---------------------------------------------------------------------
			# Make buttons sensitive again with this trick,
			# because user could have clicked on a button
			# which looked like non-sensitive while playing the video,
			# (and indeed those clicks did not act at that moment)
			# but those clicks were 'remembered' by the GTK system
			# to be fired (!) after the video window is closed ..
			# So wait a short time before making buttons sensitive again ..
			GLib.timeout_add_seconds(0.1, fnEND)
			# .. this way those clicks will be fired on a non-sensitive button !
			# ---------------------------------------------------------------------

		GLib.timeout_add_seconds(1, fnGO)
		myWindow.myButtonBVF.set_property("sensitive", False)
		myWindow.myButtonSTV.set_property("sensitive", False)
		myWindow.myButtonPOV.set_property("sensitive", False)
		myWindow.myButtonPSV.set_property("sensitive", False)
		myWindow.myButtonPUV.set_property("sensitive", False)
		myWindow.myButtonINF.set_property("sensitive", False)
		# myWindow.myButtonOPT.set_property("sensitive", False)

	# Function : User clicks button Play Stabilized Video
	def fnButtonClickedPSV(self, widget):
		# print("button PSV")

		statusINF = myWindow.myButtonINF.get_property("sensitive")
		# statusOPT = myWindow.myButtonOPT.get_property("sensitive")

		def fnGO():
			def fnEND():
				myWindow.myButtonBVF.set_property("sensitive", True)
				myWindow.myButtonSTV.set_property("sensitive", True)
				myWindow.myButtonPOV.set_property("sensitive", True)
				myWindow.myButtonPSV.set_property("sensitive", True)
				myWindow.myButtonPUV.set_property("sensitive", myWindow.myCBduo.get_active())
				myWindow.myButtonINF.set_property("sensitive", statusINF)
				# myWindow.myButtonOPT.set_property("sensitive", statusOPT)

			# the -autoexit flag causes ffplay to exit and return a status code when the audio file is done playing.
			# args = ['ffplay', '-x', '320', '-y', '180', "-autoexit", '-i', GmyVideo]

			args = []
			args.append('./ffplay_here')
			args.append('-v')
			args.append('quiet')  # -v error : this 'loglevel' gives no header info !
			args.append('-hide_banner')
			args.append('-x')
			args.append(GPXPLAYW)
			args.append('-y')
			args.append(GPXPLAYH)
			args.append('-i')
			vid = MyFuncs().rtOutPath(MyFuncs().rtStableName(MyFuncs().rtVideoFileName(GmyVideo)))
			args.append(vid)

			# subprocess.Popen(args)
			# p = subprocess.Popen(args)
			# p.wait()
			# Popen(args)  # Popen works also without subprocess
			subprocess.call(args)
			# call(args)  # call works also without subprocess

			# cmd = "ffplay \"" + GmyVideo + "\"" +"\n"
			# length = len(cmd)
			# self.terminal.feed_child(cmd, length)

			# ---------------------------------------------------------------------
			# Make buttons sensitive again with this trick,
			# because user could have clicked on a button
			# which looked like non-sensitive while playing the video,
			# (and indeed those clicks did not act at that moment)
			# but those clicks were 'remembered' by the GTK system
			# to be fired (!) after the video window is closed ..
			# So wait a short time before making buttons sensitive again ..
			GLib.timeout_add_seconds(0.1, fnEND)
			# .. this way those clicks will be fired on a non-sensitive button !
			# ---------------------------------------------------------------------

		GLib.timeout_add_seconds(1, fnGO)
		myWindow.myButtonBVF.set_property("sensitive", False)
		myWindow.myButtonSTV.set_property("sensitive", False)
		myWindow.myButtonPOV.set_property("sensitive", False)
		myWindow.myButtonPSV.set_property("sensitive", False)
		myWindow.myButtonPUV.set_property("sensitive", False)
		myWindow.myButtonINF.set_property("sensitive", False)
		# myWindow.myButtonOPT.set_property("sensitive", False)


	# Function : User clicks button Play dUo Video
	def fnButtonClickedPUV(self, widget):
		# print("button PUV")

		statusINF = myWindow.myButtonINF.get_property("sensitive")
		# statusOPT = myWindow.myButtonOPT.get_property("sensitive")

		def fnGO():
			def fnEND():
				myWindow.myButtonBVF.set_property("sensitive", True)
				myWindow.myButtonSTV.set_property("sensitive", True)
				myWindow.myButtonPOV.set_property("sensitive", True)
				myWindow.myButtonPSV.set_property("sensitive", True)
				myWindow.myButtonPUV.set_property("sensitive", myWindow.myCBduo.get_active())
				myWindow.myButtonINF.set_property("sensitive", statusINF)
				# myWindow.myButtonOPT.set_property("sensitive", statusOPT)

			# the -autoexit flag causes ffplay to exit and return a status code when the audio file is done playing.
			# args = ['ffplay', '-x', '320', '-y', '180', "-autoexit", '-i', GmyVideo]

			args = []
			args.append('./ffplay_here')
			args.append('-v')
			args.append('quiet')  # -v error : this 'loglevel' gives no header info !
			args.append('-hide_banner')
			args.append('-x')
			args.append(GPXPLAYW)
			args.append('-y')
			args.append(GPXPLAYH)
			args.append('-i')
			vid = MyFuncs().rtOutPath(MyFuncs().rtDuoName(MyFuncs().rtVideoFileName(GmyVideo)))
			args.append(vid)

			# subprocess.Popen(args)
			# p = subprocess.Popen(args)
			# p.wait()
			# Popen(args)  # Popen works also without subprocess
			subprocess.call(args)
			# call(args)  # call works also without subprocess

			# cmd = "ffplay \"" + GmyVideo + "\"" +"\n"
			# length = len(cmd)
			# self.terminal.feed_child(cmd, length)

			# ---------------------------------------------------------------------
			# Make buttons sensitive again with this trick,
			# because user could have clicked on a button
			# which looked like non-sensitive while playing the video,
			# (and indeed those clicks did not act at that moment)
			# but those clicks were 'remembered' by the GTK system
			# to be fired (!) after the video window is closed ..
			# So wait a short time before making buttons sensitive again ..
			GLib.timeout_add_seconds(0.1, fnEND)
			# .. this way those clicks will be fired on a non-sensitive button !
			# ---------------------------------------------------------------------

		GLib.timeout_add_seconds(1, fnGO)
		myWindow.myButtonBVF.set_property("sensitive", False)
		myWindow.myButtonSTV.set_property("sensitive", False)
		myWindow.myButtonPOV.set_property("sensitive", False)
		myWindow.myButtonPSV.set_property("sensitive", False)
		myWindow.myButtonPUV.set_property("sensitive", False)
		myWindow.myButtonINF.set_property("sensitive", False)
		# myWindow.myButtonOPT.set_property("sensitive", False)

