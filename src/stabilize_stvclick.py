
class STVclick(object):

	# get File SiZe
	def rtFSZ(self, path):
		# -------------------------------------------------------------------------------
		# https://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python

		# Use os.stat, and use the st_size member of the resulting object:

		# >>> import os
		# >>> statinfo = os.stat('somefile.txt')
		# >>> statinfo
		# (33188, 422511L, 769L, 1, 1032, 100, 926L, 1105022698,1105022732, 1105022732)
		# >>> statinfo.st_size
		# 926L

		# Output is in bytes.
		# -------------------------------------------------------------------------------

		statinfo = os.stat(path)
		return statinfo.st_size


	def rtVAL(self, sa, sb):  # return VALue of param sb, if found in sa, or None if not found in sa
		ix = sa.find(sb)
		if ix == -1:
			return None
		Lb = len(sb)
		ix2= ix + Lb
		s2 = sa[ix2:].strip()
		aL = s2.split(" ")
		return aL[0]


	# -------------------------------------------------------------------------------------------------
	# >> https://www.hacksparrow.com/python-check-if-a-character-or-substring-is-in-a-string.html

	# "how do you check if a substring or character is there in a string"
	# A character is also a substring technically, anyway, this is how you do it :

	# if 'c' in 'Python':
	#     print 'YES'
	# else:
	#     print 'NO'
	# Isn't that so beautifully simple?

	# When faced with the problem, my brain being damaged temporarily by PHP,
	# I started to think in terms of PHP's own substr() and strpos() functions,
	# and started looking for similar functions in Python.
	# I did get them, str.find() and str.index(),
	# but turns out they are best used when you want to know the position of the substring.
	# For checking if a substring or character exists in a string, you use the in operator instead.

	def rtTFhasSubStr(self, sa, sb):
		return sb in sa
	# -------------------------------------------------------------------------------------------------


	# Function : User clicks button STabilize Video
	def fnButtonClickedSTV(self, widget):
		global GmyVideo
		global GmsgPRGbar, GmyLog
		global GmyProcess, GmyTFprocessRun, GmyProg
		global GnrLogFPS, GnrLogSZ, GnrLogTLC

		if GmyTFprocessRun:  # CANCEL STABILIZE

			# print("button STV : CANCEL STABILIZE")
			MyFuncs().clicked_stop()

		else:  # STABILIZE

			# print("button STV : STABILIZE")
			# print("duo: "+str(myWindow.myCBduo.get_active()))
			# return  # TEST

			def fnGO():
				global GmyVideo
				global GmsgPRGbar, GmyLog
				global GmyProcess, GmyTFprocessRun, GmyProg
				global GnrLogFPS, GnrLogSZ, GnrLogTLC

				def fnEND():
					myWindow.myButtonBVF.set_property("sensitive", True)
					myWindow.myButtonPOV.set_property("sensitive", True)
					myWindow.myButtonINF.set_property("sensitive", True)
					# myWindow.myButtonOPT.set_property("sensitive", True)

				if not os.path.isdir(GdirOut):
					os.makedirs(GdirOut)

				GnrLogTLC = 0  # count # lines "too low contrast"

				# return  # TEST #############################################################


				mvGO = True  # corrected :

				try:  # TRF exists ? user can now cancel..
					vid = MyFuncs().rtOutPath(MyFuncs().rtESC(MyFuncs().rtTransformsName(MyFuncs().rtVideoFileName(GmyVideo))))
					myTRF = open(vid, "r")
					myTRF.close()
					myTRFdialog = TRFdialog(myWindow)
					myTRFresponse = myTRFdialog.run()
					myTRFdialog.destroy()

					if myTRFresponse != Gtk.ResponseType.OK:
						mvGO = False
						GmsgPRGbar = "Stabilizing cancelled .."

				except:
					# print(".trf file not found : OK")
					pass

				if mvGO:

					# 'w' This Mode Opens file for writing. 
					# If file does not exist, it creates a new file.
					# If file exists it truncates the file.
					log = open("logfile.txt", "w")

					GmyLog = ""

					# ========================================================
					# PASS 1 : create TRF file
					# ========================================================

					timeStart = time.time()  # floating-point number in units of seconds
					localtime = time.asctime( time.localtime(timeStart) )

					# print("PASS 1: CREATE TRF")

					s  = ""
					s += "START: " + localtime
					s += "\n"
					s += "\n"
					s += GstarLINE
					s += "\n"
					s += "**  "
					s += "Pass 1 of 2 : create TRF file"
					s += "\n"
					s += GstarLINE
					s += "\n"
					s += "\n"
					MyFuncs().fnLog(log, timeStart, s)

					args = []
					args.append(GmyProg)
					args.append('-hide_banner')
					args.append('-i')
					args.append(GmyVideo)
					args.append('-vf')
					trf = MyFuncs().rtOutPath(MyFuncs().rtESC(MyFuncs().rtTransformsName(MyFuncs().rtVideoFileName(GmyVideo))))
					args.append("vidstabdetect=result='"+trf+"'")
					args.append('-f')
					args.append('null')
					args.append('-')

					# print("args: " + str(args))

					myLine = ""  # use to read each transcode output line
					myLineEncLast = ""  # use to update last encountered line starting with "encoding frames [0-"
					myLineEncTotal = ""  # encounter the 1 (last) line starting with "[transcode] encoded"

					# ----------------------------------------------------------------------------------
					# frame=  165 fps=0.0 q=-0.0 size=N/A time=00:00:12.23 bitrate=N/A speed=24.2x    
					# frame=14989 fps= 85 q=27.0 size=   60928kB time=00:16:41.45 bitrate= 498.4kbits/s speed= 5.7x    
					# frame=23767 fps= 86 q=-1.0 Lsize=   94914kB time=00:26:26.03 bitrate= 490.2kbits/s speed=5.76x    

					# >> last such line always has "Lsize=N/A" :
					# frame= 3350 fps=151 q=-0.0 Lsize=N/A time=00:01:51.81 bitrate=N/A speed=5.05x  
					# ----------------------------------------------------------------------------------

					s1 = "frame="
					s1Len = len(s1)

					# video:1727kB audio:20952kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: unknown
					s3 = "muxing overhead"

					# [vidstabdetect @ 0x7ffed9eda860] too low contrast. (no translations are detected in frame 41)
					s4 = "too low contrast"  # this output appears only when creating TRF file



					nFR  = GaProbe['probeStreamsVideoNBframes'][0]
					txes = " estimated" if nFR == "[unknown]" else ""
					nFR  = GaProbe['probeStreamsVideoNBframesCalc'][0] if nFR == "[unknown]" else nFR

					tx = "creating TRF file ["+str(nFR)+" frames"+txes+"]"
					myWindow.myPRGbar.set_property("text", tx)

					# adjusted from https://stackoverflow.com/questions/1455532/ffmpeg-and-pythons-subprocess
					myWindow.myButtonSTV.set_property("label", "CANCEL")

					GmyTFprocessRun = True

					with Popen(args, stderr=PIPE) as GmyProcess:
						for line in io.TextIOWrapper(GmyProcess.stderr, newline=''):

							myLine = MyFuncs().filter_nonprintable(line)
							myLine = myLine.strip()

							if myLine != "":  # skip empty line
								myLineDSP = "[analyse]   " + myLine + "\n"

								GnrLogTLC += 1 if self.rtTFhasSubStr(myLine, s4) else 0

								s2 = myLine[:s1Len]
								if s2 == s1:  # line starts with "frame="
									nrFRM = self.rtVAL(myLine, 'frame=')
									nrFRM = int(nrFRM) if nrFRM != None else 0

									fps = self.rtVAL(myLine, ' fps=')
									fps = int(float(fps)) if fps != None else 0  # int(float(..)) because "0.0" can happen ..
									GnrLogFPS = fps

									if nFR != "[unknown]" and fps != 0:
										sec = round((int(nFR) - nrFRM) / fps)  # frames to process / speed
										tx = "analysing video ["+str(nFR)+" frames"+txes+"] ETA " + MyFuncs().rtHMS(sec)
										myWindow.myPRGbar.set_property("text", tx)

									frc = int(nrFRM) / float(nFR)
									frc = 1 if frc > 1 else frc  # may occur when # frames calculated
									myWindow.myPRGbar.set_property("fraction", frc)

									myWindow.myTXTbufferTrm.set_property("text", myLineDSP)

									myLineEncLast = myLineDSP

								else:
									MyFuncs().fnLog(log, timeStart, myLine+"\n")
									if len(myLine.split(s3)) == 2:  # line contains "muxing overhead"
										myLineEncTotal = myLineDSP

									# !?
									# Gather trancode info lines before the first encoding line;
									# they are shown as soon as the first encoding line comes (see 'if' above).
									# After the last encoding line, a few more info lines appear,
									# they are shown after this for-loop ends : see below.

							MyFuncs().fnUpdateGUI()


					txtPass1 = myLineEncLast + myLineEncTotal
					myWindow.myTXTbufferTrm.set_property("text", txtPass1)
					myWindow.myPRGbar.set_property("fraction", 1)
					# print("GmyProcess.stderr: " + str(GmyProcess.stderr))

					try:
						# trf = MyFuncs().rtOutPath(MyFuncs().rtESC(MyFuncs().rtTransformsName(MyFuncs().rtVideoFileName(GmyVideo))))
						trf = MyFuncs().rtOutPath(MyFuncs().rtTransformsName(MyFuncs().rtVideoFileName(GmyVideo)))
						sz = self.rtFSZ(trf)
						# print("sz: "+str(sz))
						GmyTFprocessRun = False if (sz == 0) else GmyTFprocessRun
					except:
						# print("sz: ERROR")
						GmyTFprocessRun = False

					if GmyTFprocessRun:

						# print("PASS 2: STABILIZE")

						# ========================================================
						# PASS 2 : stabilize video
						# ========================================================

						s  = ""
						s += "\n"
						s += GstarLINE
						s += "\n"
						s += "**  "
						s += "Pass 2 of 2 : stabilize video"
						s += "\n"
						s += GstarLINE
						s += "\n"
						s += "\n"
						MyFuncs().fnLog(log, timeStart, s)

						args = []
						args.append(GmyProg)
						args.append('-hide_banner')
						args.append('-y')  # overwrite output file if exists
						args.append('-i')
						args.append(GmyVideo)
						args.append('-vf')
						# trf = MyFuncs().rtOutPath(MyFuncs().rtESC(MyFuncs().rtTransformsName(MyFuncs().rtVideoFileName(GmyVideo))))
						trf = MyFuncs().rtOutPath(MyFuncs().rtTransformsName(MyFuncs().rtVideoFileName(GmyVideo)))
						args.append("vidstabtransform=input='"+trf+"',unsharp=5:5:0.8:3:3:0.4")
						vid = MyFuncs().rtOutPath(MyFuncs().rtStableName(MyFuncs().rtVideoFileName(GmyVideo)))
						args.append(vid)

						# print("args: " + str(args))

						myLine = ""  # use to read each transcode output line
						myLineEncLast = ""  # use to update last encountered line starting with "encoding frames [0-"
						myLineEncTotal = ""  # encounter the 1 (last) line starting with "[transcode] encoded"

						with Popen(args, stderr=PIPE) as GmyProcess:
							for line in io.TextIOWrapper(GmyProcess.stderr, newline=''):

								myLine = MyFuncs().filter_nonprintable(line)
								myLine = myLine.strip()

								# ----------------------------------------------------------------------------------
								# frame=  165 fps=0.0 q=-0.0 size=N/A time=00:00:12.23 bitrate=N/A speed=24.2x    
								# frame=14989 fps= 85 q=27.0 size=   60928kB time=00:16:41.45 bitrate= 498.4kbits/s speed= 5.7x    
								# frame=23767 fps= 86 q=-1.0 Lsize=   94914kB time=00:26:26.03 bitrate= 490.2kbits/s speed=5.76x    

								# >> last such line always has "Lsize=N/A" :
								# frame= 3350 fps=151 q=-0.0 Lsize=N/A time=00:01:51.81 bitrate=N/A speed=5.05x  
								# ----------------------------------------------------------------------------------

								if myLine != "":  # skip empty line
									myLineDSP = "[stabilize] " + myLine + "\n"

									s2 = myLine[:s1Len]
									if s2 == s1:  # line starts with "frame="
										nrFRM = self.rtVAL(myLine, 'frame=')
										nrFRM = int(nrFRM) if nrFRM != None else 0

										sz = self.rtVAL(myLine, ' size=')
										GnrLogSZ = sz if sz != None else ""

										fps = self.rtVAL(myLine, ' fps=')
										fps = int(float(fps)) if fps != None else 0  # int(float(..)) because "0.0" can happen ..
										GnrLogFPS = fps

										# print(str(nrFRM) + " *** " + str(GnrLogFPS) + " *** " + str(GnrLogSZ))

										if nFR != "[unknown]" and fps != 0:
											sec = round((int(nFR) - nrFRM) / fps)  # frames to process / speed
											tx = "stabilizing video ["+str(nFR)+" frames"+txes+"] ETA " + MyFuncs().rtHMS(sec)
											myWindow.myPRGbar.set_property("text", tx)

										frc = int(nrFRM) / float(nFR)
										frc = 1 if frc > 1 else frc  # may occur when # frames calculated
										myWindow.myPRGbar.set_property("fraction", frc)

										myWindow.myTXTbufferTrm.set_property("text", txtPass1 + myLineDSP)

										myLineEncLast = myLineDSP

									else:
										MyFuncs().fnLog(log, timeStart, myLine+"\n")
										if len(myLine.split(s3)) == 2:  # line contains "muxing overhead"
											myLineEncTotal = myLineDSP

								MyFuncs().fnUpdateGUI()

						txtPass2 = myLineEncLast + myLineEncTotal
						txtPass2 = txtPass1 + txtPass2
						myWindow.myTXTbufferTrm.set_property("text", txtPass2)

						myWindow.myPRGbar.set_property("fraction", 1)
						# print("GmyProcess.stderr: " + str(GmyProcess.stderr))


					if GmyTFprocessRun:

						if myWindow.myCBduo.get_active():

							# ========================================================
							# PASS 3 : make duo video
							# ========================================================

							s  = ""
							s += "\n"
							s += GstarLINE
							s += "\n"
							s += "**  "
							s += "make duo video"
							s += "\n"
							s += GstarLINE
							s += "\n"
							s += "\n"
							MyFuncs().fnLog(log, timeStart, s)

							# $ ffmpeg -hide_banner -i drezina1.mkv -vf "[in] pad=2*iw:ih [left]; movie=out_stable.mkv [right]; [left][right] overlay=main_w/2:0 [out]" out_both.mkv

							# ./ffmpeg -hide_banner -y -i /home/roelof/Apps/Video_Stabilizer_Python/0_example_videos/cv2.avi -vf "[in] pad=2*iw:ih [left]; movie=/home/roelof/Apps/Video_Stabilizer_Python/0_example_videos/cv2.avi.stable.mp4 [right]; [left][right] overlay=main_w/2:0 [out]" out_both.mkv

							args = []
							args.append(GmyProg)
							args.append('-hide_banner')
							args.append('-y')
							args.append('-i')
							args.append(GmyVideo)
							args.append('-vf')
							vid = MyFuncs().rtOutPath(MyFuncs().rtESC(MyFuncs().rtStableName(MyFuncs().rtVideoFileName(GmyVideo))))
							args.append('[in] pad=2*iw:ih [left]; movie='+vid+' [right]; [left][right] overlay=main_w/2:0 [out]')
							vid = MyFuncs().rtOutPath(MyFuncs().rtESC(MyFuncs().rtDuoName(MyFuncs().rtVideoFileName(GmyVideo))))
							args.append(vid)

							# print("args: " + str(args))

							myLine = ""  # use to read each transcode output line
							myLineEncLast = ""  # use to update last encountered line starting with "encoding frames [0-"
							myLineEncTotal = ""  # encounter the 1 (last) line starting with "[transcode] encoded"

							with Popen(args, stderr=PIPE) as GmyProcess:
								for line in io.TextIOWrapper(GmyProcess.stderr, newline=''):

									myLine = MyFuncs().filter_nonprintable(line)
									myLine = myLine.strip()

									# ----------------------------------------------------------------------------------
									# frame=  103 fps= 27 q=31.0 size=     256kB time=00:00:02.08 bitrate=1003.7kbits/s dup=4 drop=0 speed=0.543x

									# >> last such line always has "Lsize=N/A" :
									# frame=  261 fps= 19 q=-1.0 Lsize=    1637kB time=00:00:05.17 bitrate=2589.1kbits/s dup=4 drop=0 speed=0.368x
									# ----------------------------------------------------------------------------------

									if myLine != "":  # skip empty line
										myLineDSP = "[make duo]  " + myLine + "\n"

										s2 = myLine[:s1Len]
										if s2 == s1:  # line starts with "frame="
											nrFRM = self.rtVAL(myLine, 'frame=')
											nrFRM = int(nrFRM) if nrFRM != None else 0

											fps = self.rtVAL(myLine, ' fps=')
											fps = int(float(fps)) if fps != None else 0  # int(float(..)) because "0.0" can happen ..
											GnrLogFPS = fps

											if nFR != "[unknown]" and fps != 0:
												sec = round((int(nFR) - nrFRM) / fps)  # frames to process / speed
												tx = "making duo video ["+str(nFR)+" frames"+txes+"] ETA " + MyFuncs().rtHMS(sec)
												myWindow.myPRGbar.set_property("text", tx)

											frc = int(nrFRM) / float(nFR)
											frc = 1 if frc > 1 else frc  # may occur when # frames calculated
											myWindow.myPRGbar.set_property("fraction", frc)

											myWindow.myTXTbufferTrm.set_property("text", txtPass2 + myLineDSP)

											myLineEncLast = myLineDSP

										else:
											MyFuncs().fnLog(log, timeStart, myLine+"\n")
											if len(myLine.split(s3)) == 2:  # line contains "muxing overhead"
												myLineEncTotal = myLineDSP

									MyFuncs().fnUpdateGUI()

							txtPass3 = myLineEncLast + myLineEncTotal
							txtPass3 = txtPass2 + txtPass3
							myWindow.myTXTbufferTrm.set_property("text", txtPass3)

							myWindow.myPRGbar.set_property("fraction", 1)


						GmsgPRGbar = "process ended OK"
						myWindow.myButtonPSV.set_property("sensitive", True)  # user can see the stabilized video
						myWindow.myButtonPUV.set_property("sensitive", myWindow.myCBduo.get_active())  # user can see the duo video
						GmyTFprocessRun = False

					else:
						GmsgPRGbar = "process stopped"


					log.close()



				### myWindow.myTXTbufferTrm.set_property("text", txtPass1 + txtPass2 + GmsgPRGbar)
				myWindow.myPRGbar.set_property("text", GmsgPRGbar)
				myWindow.myTXTbufferLog.set_property("text", GmyLog)

				myWindow.myButtonSTV.set_property("label", "stabilize")

				# ---------------------------------------------------------------------
				# Make buttons sensitive again with this trick,
				# because user could have clicked on a button
				# which looked like non-sensitive while playing the video,
				# (and indeed those clicks did not act at that moment)
				# but those clicks were 'remembered' by the GTK system
				# to be fired (!) after the video window is closed ..
				# So wait a short time before making buttons sensitive again ..

				# GLib.timeout_add_seconds(0.1, fnEND)
				GLib.timeout_add_seconds(1, fnEND)
				# .. this way those clicks will be fired on a non-sensitive button !
				# ---------------------------------------------------------------------

			GLib.timeout_add_seconds(1, fnGO)
			myWindow.myButtonBVF.set_property("sensitive", False)
			myWindow.myButtonPOV.set_property("sensitive", False)
			myWindow.myButtonPSV.set_property("sensitive", False)
			myWindow.myButtonPUV.set_property("sensitive", False)
			myWindow.myButtonINF.set_property("sensitive", False)
			# myWindow.myButtonOPT.set_property("sensitive", False)

			myWindow.myPRGbar.set_property("text", "")
			myWindow.myPRGbar.set_property("fraction", 0)

			myWindow.myTXTbufferLog.set_property("text", "")

			myWindow.myTXTbufferTrm.set_property("text", "")

			myWindow.myGridOptions.hide()
			myWindow.myScrolledWindowTrm.set_property("height_request", 93)
			myWindow.myTXTmultiTrm.set_property("margin_top", 0)
			myWindow.myScrolledWindowTrm.show()
			myWindow.myPRGbar.show()
			myWindow.myScrolledWindowLog.show()

			GmyTFprocessRun = False  # init
