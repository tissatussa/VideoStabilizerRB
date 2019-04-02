# http://joequery.me/code/python-builtin-functions/#compile

myPY = 'stabilize_import.py'
myFH = open(myPY)
with myFH as f:
	contents = f.read()
myFH.close()
code_obj = compile(contents, myPY, 'exec')
exec(code_obj)

myPY = 'stabilize_var.py'
myFH = open(myPY)
with myFH as f:
	contents = f.read()
myFH.close()
code_obj = compile(contents, myPY, 'exec')
exec(code_obj)

myPY = 'stabilize_css.py'
myFH = open(myPY)
with myFH as f:
	contents = f.read()
myFH.close()
code_obj = compile(contents, myPY, 'exec')
exec(code_obj)

myPY = 'stabilize_window.py'
myFH = open(myPY)
with myFH as f:
	contents = f.read()
myFH.close()
code_obj = compile(contents, myPY, 'exec')
exec(code_obj)

myPY = 'stabilize_btnclick.py'
myFH = open(myPY)
with myFH as f:
	contents = f.read()
myFH.close()
code_obj = compile(contents, myPY, 'exec')
exec(code_obj)

myPY = 'stabilize_stvclick.py'
myFH = open(myPY)
with myFH as f:
	contents = f.read()
myFH.close()
code_obj = compile(contents, myPY, 'exec')
exec(code_obj)

myPY = 'stabilize_func.py'
myFH = open(myPY)
with myFH as f:
	contents = f.read()
myFH.close()
code_obj = compile(contents, myPY, 'exec')
exec(code_obj)

myPY = 'stabilize_dialog.py'
myFH = open(myPY)
with myFH as f:
	contents = f.read()
myFH.close()
code_obj = compile(contents, myPY, 'exec')
exec(code_obj)

myPY = 'stabilize_run.py'
myFH = open(myPY)
with myFH as f:
	contents = f.read()
myFH.close()
code_obj = compile(contents, myPY, 'exec')
exec(code_obj)
