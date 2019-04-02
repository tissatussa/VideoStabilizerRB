
class MyFuncs(object):

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
	# -------------------------------------------------------------------------------------------------
	def rtTFhasSubStr(self, sa, sb):
		return sb in sa

	def clicked_stop(self, widget=None):
		global GmyProcess, GmyTFprocessRun
		if GmyProcess:
			GmyTFprocessRun = False
			GmyProcess.terminate()
			GmyProcess.wait()

	def handle_sigterm(self, *args):
		self.clicked_stop()
		sys.exit()

	### ???
	def handle_sigsegv(self, *args):
		# print("handle_sigsegv")
		sys.exit()

	def fnLog(self, log, timeStart, s):
		global GmyLog
		log.write(MyFuncs().rtLOGtime(timeStart) + " *** " + s)
		GmyLog += s

	def fnLogFFprobe(self, log, myLine):
		log.write(myLine+"\n")

	def rtLOGtime(self, timeStart):
		timeNow = time.time()
		myTime = timeNow - timeStart
		myTime = round(myTime * 1000)
		myTime = myTime / 1000
		syTime = str(myTime)
		Ltm = syTime.split('.')
		if Ltm == 1:  # no '.' encountered : time ends with .000
			syTime += ".000"
		else:
			syMS = Ltm[1]  # MilliSeconds string, eg. '231' or '23' or '2'
			L = len(syMS)
			if L == 1: syTime += '00'
			if L == 2: syTime += '0'
		return syTime

	# https://stackoverflow.com/questions/4416336/adding-a-program-icon-in-python-gtk
	def get_resource_path(self, rel_path):
		dir_of_py_file = os.path.dirname(__file__)
		rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
		abs_path_to_resource = os.path.abspath(rel_path_to_resource)
		return abs_path_to_resource

	def filter_transcodechars(self, text):
		text = text.replace("[0m", "")
		text = text.replace("[31;1m", "")
		text = text.replace("[33;1m", "")
		text = text.replace("[34;1m", "")
		return text

	# Stripping non printable characters from a string in python
	# https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
	def filter_nonprintable(self, text):
		# Get the difference of all ASCII characters from the set of printable characters
		nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
		# Use translate to remove all non-printable characters
		text = text.translate({ord(character): None for character in nonprintable})
		text = self.filter_transcodechars(text)
		return text

	# DEV TEST #############
	def fnNONE(self):
		# print("fnNONE")
		pass

	# Function : update text buffer
	def fnUpdateGUI(self):
		# http://faq.pygtk.org/index.py?req=show&file=faq03.007.htp
		# How can I force updates to the application windows
		# during a long callback or other internal operation?
		#
		# https://stackoverflow.com/questions/14886023/gtk-messagedialog-not-closing-until-enclosing-method-finishes
		#
		# This problem is not specific to dialogs.
		# Any GUI change is invisible until you return to the main loop and give the system a chance
		# to process the events accumulated by modifying the widgets.
		# If you really want to update the GUI immediately in the callback, you can manually spin the accumulated events
		# with a loop like this after the call to dialog.destroy():
		while Gtk.events_pending():
			Gtk.main_iteration()

	# is 'ffmpeg' installed on the user system ?
	def rtLineFFinstalled(self):
		global GmyProg

		NRlines = 0
		sLines = ""  # gather all lines
		sRTline = ""  # return line

		GmyProg = ""  # default : use FFmpeg binairy by $PATH
		fh = open("./stabilize.cfg")  # find FFmpeg binairy path in config file ("prog=" can be empty here)
		with fh as f: 
			for line in f:
				sCFG = 'prog='
				if line[:len(sCFG)] == sCFG:
					GmyProg = line[len(sCFG):].strip()  # could be empty : use FFmpeg binairy by $PATH

		fh.close()

		if GmyProg == "":
			# print("default : use FFmpeg binairy by $PATH")
			args = ['ffmpeg']  # use FFmpeg binairy by $PATH
		else:
			# print("stabilize.cfg : use FFmpeg binairy by absolute path")
			args = [GmyProg]  # use FFmpeg binairy by absolute path

		args.append('-version')

		try:
			# adjusted from https://stackoverflow.com/questions/1455532/ffmpeg-and-pythons-subprocess
			process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

			for line in process.stdout:
				if NRlines == 0:
					sRTline = line.rstrip()
				sLines += line
				NRlines += 1

			if len(sLines.split('--enable-libvidstab')) != 2:
				sRTline = "noVidStab"

		except:
			sRTline = "noFFmpeg"

		return sRTline

	def rtESC(self, s):
		# https://ffmpeg.org/ffmpeg-utils.html#Quoting-and-escaping

		# Escape the string Crime d'Amour containing the ' special character:
		# Crime d\'Amour
		# The string above contains a quote, so the ' needs to be escaped when quoting it:
		# 'Crime d'\''Amour'
		return s.replace("'", "'\\''")

	def rtOutPath(self, file):
		return GdirOut + '/' + file

	def rtVideoFileName(self, path):
		aMV = path.split("/")
		return aMV[len(aMV)-1]

	def rtStableName(self, s):
		s += '.stable.mp4'
		return s

	def rtTransformsName(self, s):
		s += '.transforms.trf'
		return s

	def rtDuoName(self, s):
		s += '.duo.mp4'
		return s

	def rtTwoDigits(self, i):
		if i < 10:
			return "0" + str(i)
		return str(i)

	def rtHMS(self, sec):

		# sec2 = 8100  # 02:15:00
		sec2 = sec  # 02:15:00

		# nrS = 0
		# print(str(140 % 60))  # 20
		# print(str(60 % 140))  # 60

		nrS = sec2 % 60  # 0
		# print("nrS: "+str(nrS))

		nrM1 = round((sec2 - nrS) / 60)
		# print("nrM1: "+str(nrM1))  # 135

		nrM2 = nrM1 % 60  # 15
		# print("nrM2: "+str(nrM2))  # 15

		nrH = round((nrM1 - nrM2) / 60)
		# print("nrH: "+str(nrH))

		return MyFuncs().rtTwoDigits(nrH) + ":" + MyFuncs().rtTwoDigits(nrM2) + ":" + MyFuncs().rtTwoDigits(nrS)
		# return str(sec)


	# LV : Loaded Video : update info and buttons
	def fnSetLVline(self, widget):
		global GmyVideo

		res = MyFuncs().rtVideoFFprobe(GmyVideo)  # returns 'ok' / 'fail'
		if res == 'ok':
			# print("fnSetLVline() video OK")
			pass
		else:  # 'fail'
			# print("fnSetLVline() video FAIL")
			GmyVideo = ""

		if GmyVideo == "":
			LVtxt = "[none]"
			LVtt = "please browse a video file"
			widget.myButtonSTV.set_property("sensitive", False)
			widget.myButtonPOV.set_property("sensitive", False)
			widget.myButtonINF.set_property("sensitive", False)
			# widget.myButtonOPT.set_property("sensitive", False)

		else:  # file can be pre-selected in stabilize_var.py .. we assume its path is valid
			LVtxt = MyFuncs().rtVideoFileName(GmyVideo)
			LVtt  = MyFuncs().rtVideoMeta()
			widget.myButtonSTV.set_property("sensitive", True)
			widget.myButtonPOV.set_property("sensitive", True)
			widget.myButtonINF.set_property("sensitive", True)
			# widget.myButtonOPT.set_property("sensitive", True)

		widget.myButtonPSV.set_property("sensitive", False)
		widget.myButtonPUV.set_property("sensitive", False)
		widget.myTXTentryLV.set_property("text", svTXT + " : " + LVtxt)
		widget.myTXTentryLV.set_property("tooltip_text", LVtt)


	def rtLVTTline(self, item):
		if GaProbe[item][0] == "[unknown]":
			return GaProbe[item][1]+": [unknown]"
		return GaProbe[item][1]+": " + str(GaProbe[item][0]) + " " + GaProbe[item][2]

	def rtLVTTlineDR(self):  # DURation
		# ffprobe option -sexagesimal : use format HOURS:MM:SS.MICROSECONDS for time units

		# As long as your numbers are positive, you can simply convert to an int to round down to the next integer:
		# >>> int(3.1415)
		# 3

		dur = GaProbe['probeFormatDuration'][0]
		if dur == "[unknown]":
			return GaProbe['probeFormatDuration'][1] + ": [unknown]"
		dur = float(dur)  # float : seconds
		Hz  = int( dur / (60*60))
		Mz  = int((dur - (Hz * 60 * 60)            ) / 60)
		Sz  = round( dur - (Hz * 60 * 60) - (Mz * 60),2)
		sH  = "0"+str(Hz) if Hz < 10 else str(Hz)
		sM  = "0"+str(Mz) if Mz < 10 else str(Mz)
		sS  = "0"+str(Sz) if Sz < 10 else str(Sz)
		return str(GaProbe['probeFormatDuration'][1]) + " (HH:MM:SS.nn): " + sH+":"+sM+":"+sS

	def rtLVTTlineSZ(self):  # SiZe
		sz = GaProbe['probeFormatSize'][0]
		if sz == "[unknown]":
			return GaProbe['probeFormatSize'][1] + ": [unknown]"
		sz = int(sz)
		if sz > 1000000000:
			tx = str(round(sz / 1000000000,2)) + " Gb"
		elif sz > 1000000:
			tx = str(round(sz / 1000000,2)) + " Mb"
		elif sz > 1000:
			tx = str(round(sz / 1000,2)) + " Kb"
		else:
			tx = str(sz) + " bytes"
		return str(GaProbe['probeFormatSize'][1]) + ": " + tx

	def rtLVTTlineBR(self, item):  # BitRate in Kbit/s ### item: audio / video
		br = GaProbe[item][0]
		if br == "[unknown]":
			return GaProbe[item][1] + ": [unknown]"
		br = str(round(int(br) / 1000, 2)) + " " + GaProbe[item][2]
		return str(GaProbe[item][1]) + ": " + br

	def rtLVTTlineWH(self):
		return "frame size (width x height): " + str(GaProbe['probeStreamsVideoWidth'][0]) + " x " + str(GaProbe['probeStreamsVideoHeight'][0]) + " " + GaProbe['probeStreamsVideoWidth'][2]

	def rtVideoMeta(self):  # ToolTip info
		LVtt  = "path: " + GmyVideo
		LVtt += "\n"
		LVtt += "\n=== general / video info =========================="
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoIsAVC')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoCodecTagString')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeFormatName')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeFormatNameLong')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoCodecName')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoCodecNameLong')
		LVtt += "\n"+MyFuncs().rtLVTTlineDR()
		# LVtt += "\n"+MyFuncs().rtLVTTline('probeFormatDuration')
		LVtt += "\n"+MyFuncs().rtLVTTlineSZ()
		# LVtt += "\n"+MyFuncs().rtLVTTline('probeFormatSize')
		LVtt += "\n"+MyFuncs().rtLVTTlineWH()
		# LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoWidth')
		# LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoHeight')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoPixFmt')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoSampleAspectRatio')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoDisplayAspectRatio')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoAvgFrameRate')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoAvgFrameRateInt')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoNBframes')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoNBframesCalc')
		# LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoBitRate')
		LVtt += "\n"+MyFuncs().rtLVTTlineBR('probeStreamsVideoBitRate')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsVideoFieldOrder')
		LVtt += "\n"
		LVtt += "\n=== audio info ===================================="
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsAudioCodecName')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsAudioCodecNameLong')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsAudioChannels')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsAudioSampleRate')
		# LVtt += "\n"+MyFuncs().rtLVTTline('probeStreamsAudioBitRate')
		LVtt += "\n"+MyFuncs().rtLVTTlineBR('probeStreamsAudioBitRate')
		LVtt += "\n"
		LVtt += "\n=== meta info ====================================="
		LVtt += "\n"+MyFuncs().rtLVTTline('probeTagsLNG')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeTagsHDN')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeTagsMBR')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeTagsCBR')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeTagsCTM')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeTagsENC')
		LVtt += "\n"+MyFuncs().rtLVTTline('probeTagsTTL')

		return LVtt


	def rtVideoFFprobe(self, vid):  # returns 'ok' / 'fail'
		global GaProbe

		if vid == "":
			# print("### rtVideoFFprobe : video file empty : FAIL A")
			return 'fail'

		# >> https://www.bugcodemaster.com/article/use-ffprobe-obtain-information-video-files

		# ./ffprobe_here -v error -show_streams -show_format -of json -i ../0_example_videos/
		args = []
		args.append('./ffprobe_here')
		args.append('-v')
		args.append('quiet')  # -v error : this 'loglevel' gives no header info !
		args.append('-hide_banner')
		args.append('-show_format')
		args.append('-show_streams')
		# args.append('-sexagesimal')
		# args.append('-unit')  # for test
		args.append('-of')
		args.append('json')
		# args.append('json:string_validation_replacement="Q"')  # ??
		args.append('-i')
		args.append(vid)

		# adjusted from https://stackoverflow.com/questions/1455532/ffmpeg-and-pythons-subprocess
		process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

		sOut = ""
		log = open("ffprobe_json.txt", "w")
		# 'w' This Mode Opens file for writing. 
		# If file does not exist, it creates a new file.
		# If file exists it truncates the file.

		for line in process.stdout:
			myLine = MyFuncs().filter_nonprintable(line)
			MyFuncs().fnLogFFprobe(log, myLine)
			sOut += myLine
		log.close()
		aData = json.loads(sOut)

		GaProbe = {}  # value, item name, units
		# GaProbe['probeStreamsVideoProfiles'] = []

		# DEFAULTS
		# first get tags in (main) video track, then update this info (no overwrite) with tags info of format section.
		# the following tags are often found in video tracks and format section :
		GaProbe['probeTagsLNG'] = ("[unknown]", "language", "")
		GaProbe['probeTagsHDN'] = ("[unknown]", "handler name", "")
		GaProbe['probeTagsMBR'] = ("[unknown]", "major brand", "")
		GaProbe['probeTagsCBR'] = ("[unknown]", "compatible brands", "")
		GaProbe['probeTagsCTM'] = ("[unknown]", "creation time", "")
		GaProbe['probeTagsENC'] = ("[unknown]", "encoder", "")
		GaProbe['probeTagsTTL'] = ("[unknown]", "title", "")

		GaProbe['probeStreamsAudioCodecName']     = ("[unknown]", "codec name", "")
		GaProbe['probeStreamsAudioCodecNameLong'] = ("[unknown]", "codec long name", "")
		GaProbe['probeStreamsAudioChannels']      = ("[unknown]", "channels", "")
		GaProbe['probeStreamsAudioSampleRate']    = ("[unknown]", "sample rate", "Hz")
		GaProbe['probeStreamsAudioBitRate']       = ("[unknown]", "bit rate", "kbit/s")

		TFvideo = False
		TFaudio = False

		for streamIX in aData['streams']:
			sAV = streamIX.get('codec_type', "[unknown]")
			if sAV == 'video':

				if not TFvideo:  # when multi video tracks : get first ('Main' / 'High' / '0' / 'Profile 0' / 'Advanced Simple Profile' / etc !? )
					# GaProbe['probeStreamsVideoProfile']            = (streamIX.get('profile', "[unknown]"), "profile", "")

					GaProbe['probeStreamsVideoFieldOrder']         = (streamIX.get('field_order', "[unknown]"), "field order", "")
					GaProbe['probeStreamsVideoCodecName']          = (streamIX.get('codec_name', "[unknown]"), "codec name", "")
					GaProbe['probeStreamsVideoCodecNameLong']      = (streamIX.get('codec_long_name', "[unknown]"), "codec long name", "")
					GaProbe['probeStreamsVideoCodecTagString']     = (streamIX.get('codec_tag_string', "[unknown]"), "codec tag string", "")
					GaProbe['probeStreamsVideoWidth']              = (streamIX.get('width', "[unknown]"), "width", "px")
					GaProbe['probeStreamsVideoHeight']             = (streamIX.get('height', "[unknown]"), "height", "px")
					GaProbe['probeStreamsVideoSampleAspectRatio']  = (streamIX.get('sample_aspect_ratio', "[unknown]"), "sample aspect ratio", "")
					GaProbe['probeStreamsVideoDisplayAspectRatio'] = (streamIX.get('display_aspect_ratio', "[unknown]"), "display aspect ratio", "")
					GaProbe['probeStreamsVideoPixFmt']             = (streamIX.get('pix_fmt', "[unknown]"), "pix fmt", "")
					GaProbe['probeStreamsVideoIsAVC']              = (streamIX.get('is_avc', "[unknown]"), "is avc", "")

					pafr = streamIX.get('avg_frame_rate', "[unknown]")
					GaProbe['probeStreamsVideoAvgFrameRate']       = (pafr, "avg frame rate", "")

					pafrInt = 0  # corrected
					L = pafr.split('/')
					if len(L) != 1:  # should contain char '/'
						if L[0] != '0' and L[1] != '0':
							pafrInt = round(int(L[0]) / int(L[1]), 2)

					GaProbe['probeStreamsVideoAvgFrameRateInt']    = (pafrInt, "avg frame rate (number)", "fps")

					GaProbe['probeStreamsVideoBitRate']            = (streamIX.get('bit_rate', "[unknown]"), "bit rate", "kbit/s")
					GaProbe['probeStreamsVideoNBframes']           = (streamIX.get('nb_frames', "[unknown]"), "# frames", "")

					tags = streamIX.get('tags', "[unknown]")
					if tags != "[unknown]":
						z = streamIX['tags'].get('language', "[unknown]")
						z = streamIX['tags'].get('LANGUAGE', "[unknown]") if z == "[unknown]" else z
						if z != "[unknown]":
							GaProbe['probeTagsLNG'] = (z, "language", "")

						z = streamIX['tags'].get('handler_name', "[unknown]")
						z = streamIX['tags'].get('HANDLER_NAME', "[unknown]") if z == "[unknown]" else z
						if z != "[unknown]":
							GaProbe['probeTagsHDN'] = (z, "handler name", "")

						z = streamIX['tags'].get('major_brand', "[unknown]")
						z = streamIX['tags'].get('MAJOR_BRAND', "[unknown]") if z == "[unknown]" else z
						if z != "[unknown]":
							GaProbe['probeTagsMBR'] = (z, "major brand", "")

						z = streamIX['tags'].get('compatible_brands', "[unknown]")
						z = streamIX['tags'].get('COMPATIBLE_BRANDS', "[unknown]") if z == "[unknown]" else z
						if z != "[unknown]":
							GaProbe['probeTagsCBR'] = (z, "compatible brands", "")

						z = streamIX['tags'].get('creation_time', "[unknown]")
						z = streamIX['tags'].get('CREATION_TIME', "[unknown]") if z == "[unknown]" else z
						if z != "[unknown]":
							GaProbe['probeTagsCTM'] = (z, "creation time", "")

						z = streamIX['tags'].get('encoder', "[unknown]")
						z = streamIX['tags'].get('ENCODER', "[unknown]") if z == "[unknown]" else z
						if z != "[unknown]":
							GaProbe['probeTagsENC'] = (z, "encoder", "")

						z = streamIX['tags'].get('title', "[unknown]")
						z = streamIX['tags'].get('TITLE', "[unknown]") if z == "[unknown]" else z
						if z != "[unknown]":
							GaProbe['probeTagsTTL'] = (z, "title", "")


				# GaProbe['probeStreamsVideoProfiles'].append(streamIX.get('profile', "[unknown]"))
				TFvideo = True

			if sAV == 'audio':

				GaProbe['probeStreamsAudioCodecName']          = (streamIX.get('codec_name', "[unknown]"), "codec name", "")
				GaProbe['probeStreamsAudioCodecNameLong']      = (streamIX.get('codec_long_name', "[unknown]"), "codec long name", "")
				GaProbe['probeStreamsAudioChannels']           = (streamIX.get('channels', "[unknown]"), "channels", "")
				GaProbe['probeStreamsAudioSampleRate']         = (streamIX.get('sample_rate', "[unknown]"), "sample rate", "Hz")
				GaProbe['probeStreamsAudioBitRate']            = (streamIX.get('bit_rate', "[unknown]"), "bit rate", "kbit/s")

				TFaudio = True

		if not TFvideo:
			# print("### rtVideoFFprobe : video file empty : FAIL B")
			return 'fail'


		GaProbe['probeFormatName']     = (aData['format'].get('format_name', "[unknown]"), "format name", "")
		GaProbe['probeFormatNameLong'] = (aData['format'].get('format_long_name', "[unknown]"), "format long name", "")
		GaProbe['probeFormatDuration'] = (aData['format'].get('duration', "[unknown]"), "duration", "sec.")
		GaProbe['probeFormatSize']     = (aData['format'].get('size', "[unknown]"), "size", "byte")

		tags = aData['format'].get('tags', "[unknown]")
		if tags != "[unknown]":
			z = aData['format']['tags'].get('language', "[unknown]")
			z = aData['format']['tags'].get('LANGUAGE', "[unknown]") if z == "[unknown]" else z
			if z != "[unknown]" and GaProbe['probeTagsLNG'][0] == "[unknown]":
				GaProbe['probeTagsLNG'] = (z, "language", "")

			z = aData['format']['tags'].get('handler_name', "[unknown]")
			z = aData['format']['tags'].get('HANDLER_NAME', "[unknown]") if z == "[unknown]" else z
			if z != "[unknown]" and GaProbe['probeTagsHDN'][0] == "[unknown]":
				GaProbe['probeTagsHDN'] = (z, "handler name", "")

			z = aData['format']['tags'].get('major_brand', "[unknown]")
			z = aData['format']['tags'].get('MAJOR_BRAND', "[unknown]") if z == "[unknown]" else z
			if z != "[unknown]" and GaProbe['probeTagsMBR'][0] == "[unknown]":
				GaProbe['probeTagsMBR'] = (z, "major brand", "")

			z = aData['format']['tags'].get('compatible_brands', "[unknown]")
			z = aData['format']['tags'].get('COMPATIBLE_BRANDS', "[unknown]") if z == "[unknown]" else z
			if z != "[unknown]" and GaProbe['probeTagsCBR'][0] == "[unknown]":
				GaProbe['probeTagsCBR'] = (z, "compatible brands", "")

			z = aData['format']['tags'].get('creation_time', "[unknown]")
			z = aData['format']['tags'].get('CREATION_TIME', "[unknown]") if z == "[unknown]" else z
			if z != "[unknown]" and GaProbe['probeTagsCTM'][0] == "[unknown]":
				GaProbe['probeTagsCTM'] = (z, "creation time", "")

			z = aData['format']['tags'].get('encoder', "[unknown]")
			z = aData['format']['tags'].get('ENCODER', "[unknown]") if z == "[unknown]" else z
			if z != "[unknown]" and GaProbe['probeTagsENC'][0] == "[unknown]":
				GaProbe['probeTagsENC'] = (z, "encoder", "")

			z = aData['format']['tags'].get('title', "[unknown]")
			z = aData['format']['tags'].get('TITLE', "[unknown]") if z == "[unknown]" else z
			if z != "[unknown]" and GaProbe['probeTagsTTL'][0] == "[unknown]":
				GaProbe['probeTagsTTL'] = (z, "title", "")


		nbfc = "[unknown]"  # corrected:
		if GaProbe['probeFormatDuration'][0] != "[unknown]" and GaProbe['probeStreamsVideoAvgFrameRateInt'][0] != 0:
			nbfc = round(float(GaProbe['probeFormatDuration'][0]) * GaProbe['probeStreamsVideoAvgFrameRateInt'][0])
		GaProbe['probeStreamsVideoNBframesCalc'] = (nbfc, "# frames (calculated)", "")

		return 'ok'



	# http://www.programcreek.com/python/example/615/webbrowser.open
	# Example 29
	# better : the pychess source at https://sourceforge.net/projects/pychess/
	# NOTE: we need 2 extra vars : 'linkre' and 'emailre' : see pychess source and my stabilize_var.py
	def initTexviewLinks(self, textview, text):
		global linkre, emailre

		tags = []
		textbuffer = textview.get_buffer()
		
		while True:
			linkmatch = linkre.search(text)
			emailmatch = emailre.search(text)
			if not linkmatch and not emailmatch:
				textbuffer.insert(textbuffer.get_end_iter(), text)
				# print("### no more links found")
				break
			
			# print("### a link found")
			if emailmatch and (not linkmatch or emailmatch.start() < linkmatch.start()):
				s = emailmatch.start()
				e = emailmatch.end()
				myType = "email"
			else:
				s = linkmatch.start()
				e = linkmatch.end()
				if text[e-1] == ".":
					e -= 1
				myType = "link"
			textbuffer.insert(textbuffer.get_end_iter(), text[:s])

			# Gtk3 TextBuffer.serialize() returns text with format tags, even when there is visually none
			# https://stackoverflow.com/questions/30387247/gtk3-textbuffer-serialize-returns-text-with-format-tags-even-when-there-is-vi
			# MORE :
			# tag_bold = textBodyBuffer.create_tag("bold", weight=Pango.Weight.BOLD)
			# tag_italic = textBodyBuffer.create_tag("italic", style=Pango.Style.ITALIC)
			# tag_underline = textBodyBuffer.create_tag("underline", underline=Pango.Underline.SINGLE)
			tag = textbuffer.create_tag(None, foreground="yellow", underline=Pango.Underline.SINGLE)
			tags.append([tag, text[s:e], myType, textbuffer.get_end_iter()])
			
			textbuffer.insert_with_tags(textbuffer.get_end_iter(), text[s:e], tag)
			
			tags[-1].append(textbuffer.get_end_iter())
			
			text = text[e:]
		
		def on_press_in_textview(textview, event):
			myIter = textview.get_iter_at_location(int(event.x), int(event.y))
			if not myIter: return
			for tag, link, myType, s, e in tags:
				if myIter.has_tag(tag):
					tag.set_property("foreground", "red")
					break
		
		def on_release_in_textview(textview, event):
			myIter = textview.get_iter_at_location(int(event.x), int(event.y))
			if not myIter: return
			for tag, link, myType, s, e in tags:
				if myIter.has_tag(tag) and tag.get_property("foreground_gdk").red == 65535:
					if myType == "link":
						webbrowser.open_new_tab(link)
					else: webbrowser.open("mailto:"+link)
				tag.set_property("foreground", "yellow")

		def on_motion_in_textview(textview, event):
			global textcursor, linkcursor, TWTtext
			textview.get_pointer()
			myIter = textview.get_iter_at_location(int(event.x), int(event.y))
			if not myIter: return
			for tag, link, myType, s, e in tags:
				if myIter.has_tag(tag):
					tag.set_property("background", "blue")

					# https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextView.html#Gtk.TextView.get_window
					# get_window(win)
					# Parameters:  win (Gtk.TextWindowType) – window to get
					# Returns:     a Gdk.Window, or None
					# Return type: Gdk.Window or None
					textview.get_window(TWTtext).set_cursor(linkcursor)
					break
				else:
					tag.set_property("background", None)
					textview.get_window(TWTtext).set_cursor(textcursor)

		textview.connect("motion-notify-event", on_motion_in_textview)
		textview.connect("leave_notify_event", on_motion_in_textview)
		textview.connect("button_press_event", on_press_in_textview)
		textview.connect("button_release_event", on_release_in_textview)

