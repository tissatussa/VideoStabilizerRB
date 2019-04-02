
GTXTinfo = "Stabilize Video v0.2a"

GdirOut = "./output"  # will be created if not exists


# =====================================================================================
# .desktop launcher file contents.
# NOTE: Exec line has %F : first parameter is (video) file to open at right click in Filemanager !
#       When the .desktop file is placed in (HOME) .local/share/applications, the program wlll appear in Ubuntu "open with" dialogs !

# [Desktop Entry]
# Version=1.0
# Type=Application
# Terminal=false
# StartupNotify=true
# Name[en_US]=Stabilize Video
# Exec=python3 /home/roelof/Apps/Video_Stabilizer_Python/now/stabilize_launch.py %F
# Path=/home/roelof/Apps/Video_Stabilizer_Python/now/
# Categories=Utility;Application;
# Comment=stabilize any video with ffmpeg and vidstab module
# Icon=/home/roelof/Apps/Video_Stabilizer_Python/now/icon.png
# =====================================================================================

# >> https://www.tutorialspoint.com/python/python_command_line_arguments.htm
GmyVideo = "" if len(sys.argv) == 1 else sys.argv[1]

# GmyVideo = ""  # default empty string : user should browse a video
# ### for TEST : here you can give some video (complete path) : no browse needed
# GmyVideo = "/home/roelof/Projects/PyCharm/PRJb/part1_mini_1280x720_50fps.m4v"
# GmyVideo = "/home/roelof/Projects/PyCharm/PRJb/Anastasia_film.mp4"
# =====================================================================================




GmyFFnoTXT   = "The program 'ffmpeg' is not found on your system - you can not use this application .."
GmyFFVSnoTXT = "The program 'ffmpeg' is found on your system but has no vid.stab module - you can not use this application .."
svTXT = "selected video"

GPXPLAYW = '640'
GPXPLAYH = '360'

GmyProcess = None  # Initialize the handle to our (sub)process
GmyTFprocessRun = False

GmyLog = ""

GnrLogTLC  = 0

GnrLogFPS  = 0
GnrLogSZ   = 0

GmsgPRGbar = ""


# https://stackoverflow.com/questions/6328990/change-cursor-type-in-pygtk-application#7857072
# https://lazka.github.io/pgi-docs/#Gdk-3.0/enums.html#Gdk.CursorType
# https://developer.gnome.org/gdk3/stable/gdk3-Cursors.html#GdkCursorType
textcursor = Gdk.Cursor(Gdk.CursorType.XTERM)
linkcursor = Gdk.Cursor(Gdk.CursorType.HAND2)

# https://lazka.github.io/pgi-docs/Gtk-3.0/enums.html#Gtk.TextWindowType.TEXT
TWTtext = Gtk.TextWindowType(2)  # 2 : TEXT : Scrollable text window
# print(str(type(textviewZ.get_window(TWTtext))))  # <class 'gi.repository.GdkX11.X11Window'>


GtrmTXT  = ""
GtrmTXT += "This application can stabilize any (*) video, so-called 'deshaking'.\n"
GtrmTXT += "It uses the famous FFMPEG program, which is compiled with the 'vidstab' module.\n"
GtrmTXT += "*) Many common video formats are supported: .mp4 .mkv .mov .mpg .mpeg .asf .flv .wmv, etc.\n"

# >> https://ffmpeg.org/ffplay-all.html
GinfoTXT  = ""
GinfoTXT += "-----------------------------------------\n"
GinfoTXT += "Key / mouse actions while playing a video\n"
GinfoTXT += "-----------------------------------------\n"
GinfoTXT += "q, ESC                      : quit\n"
GinfoTXT += "f, left mouse double-click  : toggle full screen\n"
GinfoTXT += "p, spacebar                 : pause\n"
GinfoTXT += "m                           : toggle audio mute\n"
GinfoTXT += "9, 0                        : decrease / increase volume\n"
GinfoTXT += "/, *                        : decrease / increase volume\n"
GinfoTXT += "s                           : (pause and) step to the next frame\n"
GinfoTXT += "arrow left / right          : seek backward / forward 10 seconds\n"
GinfoTXT += "arrow down / up             : seek backward / forward 1 minute\n"
GinfoTXT += "PgDn / PgUp                 : seek to previous / next chapter,\n"
GinfoTXT += "                              or seek backward / forward 10 minutes if there are no chapters.\n"
GinfoTXT += "right mouse click           : seek to percentage in file corresponding to fraction of width"



GaProbe = []  # gather video / audio info by ffprobe

# defaults ffprobe video
# probeFrames = 0
# probeDuration = "0:00:00.000000"
# probeWidth = 0
# probeHeight = 0
# probeSampleAspectRatio = '0:0'
# probeDisplayAspectRatio = '0:0'
# probeCodecName = "[unknown]"
# probeCodecNameLong = "[unknown]"
# probeCodecTagString = "[unknown]"
# probePixFmt = "[unknown]"
# probeIsAVC = "false"  # might be detected 'true' or not-given (>> 'false')
# probeAvgFrameRate = "0/0"
# probeAvgFrameRateInt = 0
# probeBitrate = "N/A"  # eg. when WebM / ASF

# defaults ffprobe audio
# probeAudioCodecName = "unknown"
# probeAudioCodecNameLong = "unknown"
# probeAudioCodecTagString = "unknown"
# probeAudioChannels = 0
# probeAudioBitrate = 0
# probeAudioSampleRate = 0

# linkre = re.compile("http://(?:www\.)?\w+\.\w{2,4}[^\s]+")  # ORG
linkre  = re.compile("http(?:s)?://(?:www\.)?\w+\.\w{2,4}[^\s]+")
emailre = re.compile("[\w\.]+@[\w\.]+\.\w{2,4}")

GstarLINE = "************************************************"

