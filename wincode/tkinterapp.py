import tkinter
from tkinter import ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkfont
from tkinter import StringVar
from tkinter.ttk import Style
from tkinter import Toplevel

#-------------------------------tkinter---------------
from tkinter.scrolledtext import ScrolledText
import time
import os
import sqlite3
from threading import Thread

from collections import Counter
from queue import Queue
#-------------------------------python standard---------------
import keyboard
from PIL import ImageTk, Image
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import webview


#------------------------third party----------------
Base = declarative_base()

'''note = ttk.Notebook(self)
save still work?

		tab1 = tkinter.Frame(note)
		tab2 = tkinter.Frame(note)
		tab3 = tkinter.Frame(note)
		tkinter.Button(tab1, text='Exit', command=self.destroy).pack(padx=100, pady=100)

		note.add(tab1, text = "Tab One")
		note.add(tab2, text = "Tab Two")
		note.add(tab3, text = "Tab Three")
		note.grid(sticky='n')

engine = create_engine('sqlite:///tkinterapp.db')

Base.metadata.create_all(engine)
Base.metadata.bind = engine

dbsession = sessionmaker(bind=engine)
		
session = dbsession()'''




#-----------------------Load out/info page-------------------------
class recent(Base):
	__tablename__ = 'recentfiles'
	id = Column(Integer, primary_key=True)
	recentfiles = Column(String(50))
	currentdir = Column(String(50))
	

class main(tkinter.Tk):
	
	def __init__(self, *args, **kwargs):
		tkinter.Tk.__init__(self, *args, **kwargs)
		frame = tkinter.Frame(self)   
		main.LandingPage(self, frame)
		s = Style()
		s.theme_use('xpnative')
		

		


	def LandingPage(self, frame):
		h = lambda: controlers.shiftpage(self, frame, function=navigation)
		self.geometry('300x500+600+300')
		self.resizable(0,0)
		#editControls()
		
		label = tkinter.Label(self, text='Welcome to wincode \n A custom text editor for python', foreground='blue')
		label.pack()
		main.img = ImageTk.PhotoImage(Image.open("images.jpg"))
		#canvas.create_image(20, 20, anchor='nw', image=main.img)
		lab = tkinter.Label(self, image=main.img)
		lab.pack(pady='40')
		button = tkinter.Button(self, text='Start Programming', command=h)
		button.pack(pady='40')
		yearlabel = tkinter.Label(text='November 2018')
		yearlabel.pack()
		#testing messagebox
		#messagebox.showerror("Error", "Error message")
		#messagebox.showwarning("Warning","Warning message")
		#messagebox.showinfo("Information","Informative message")
		#main.waiting(self, frame)
		s = Style()
		s.theme_use('clam')
		#--------------------------database------------------------------
class controlers:
	def __init__():
		print('did the controlers init actually run?')
		
	def sessionmanager(currentdir=None, recentfiles=None, query=False):
		from collections import OrderedDict
		
		engine = create_engine('sqlite:///tkinterapp.db')

		Base.metadata.create_all(engine)
		Base.metadata.bind = engine

		dbsession = sessionmaker(bind=engine)
		
		session = dbsession()
		global_output = OrderedDict()
		
		if recentfiles != None and currentdir != None and query == False:
			addit = recent(currentdir=str(currentdir), recentfiles=str(recentfiles))
			session.add(addit)
			session.commit()
			return recentfiles
		if query == False and currentdir == 'none':
			add_dir = recent(currentdir=None)
			session.add(add_dir)
			session.commit()
		elif query == False and currentdir != None:
			add_dir = recent(currentdir=str(currentdir))
			session.add(add_dir)
			session.commit()
		elif query == True and currentdir == 'Query':
			output = session.query(recent.currentdir).all()
			global_output['current'] = output
			for item in output:
				newval=item
			for items in newval:

				
				newvals = items
			return newvals
		
			
		
		if query == False and recentfiles != None:
			add_dir = recent(recentfiles=str(recentfiles))
			session.add(add_dir)
			session.commit()
		elif query == True and recentfiles == 'Query':
			output2 = session.query(recent.recentfiles).all()
			global_output['recent'] = output2
			filtered = []
			for item in output2:
				for items in item:
					if items != None:
						filtered.append(items)
			sortedout = Counter(filtered).most_common()
			print('sortedout')
			return sortedout
		
		
	#--------------------open and highlight text editor/load attached notes------------------
	def openfiles(box, directory, notes=None, title=None):
		check = 'block'

		if notes == None:
			messagebox.showinfo('cant be empty', 'you need to add something first')
		elif str(directory) == '':
			pass
			
		else:
			box.delete('1.0', 'end')
			title['text'] = str(directory)
			with open(str(directory), 'r') as file:
				for count, item in enumerate(file):
							
					item = item.replace('	', '\t')
					if '#' in str(item) and check == 'block':
						#print(item)
						#box.tag_add("here", "first", "last")
						
						box.insert('end', str(item))
						box.tag_add("here", str(float(count +1)), str(float(count+2)))
						box.tag_config("here", foreground="red")
						
						#box.tag_config("start", background="black", foreground="green")
				
					elif "'" * 3 in str(item) and check == 'block':
						box.insert('end', str(item))
						box.tag_add("here1", str(float(count +1)), str(float(count+2)))
						box.tag_config("here1", foreground="red")
						check = 'activeblock'
					elif check == 'activeblock' and "'" * 3 not in str(item):
						box.insert('end', str(item))
						box.tag_add("here2", str(float(count +1)), str(float(count+2)))
						box.tag_config("here2", foreground="red")
					elif "'" * 3 in str(item) and check == 'activeblock':
						check = 'block'
						box.insert('end', str(item))
						box.tag_add("here2", str(float(count +1)), str(float(count+2)))
						box.tag_config("here2", foreground="red")
				   	
					elif '\tdef ' in str(item) and check == 'block':
						
						box.insert('end', str(item))
						box.tag_add("here3", str(float(count +1)), str(float(count+2)))
						box.tag_config("here3", foreground="blue")
					elif 'cla' + ('s' *2) + ' ' in str(item) and check == 'block' and ':' in str(item):
						box.insert('end', str(item))
						box.tag_add('hclasses', str(float(count+1)), str(float(count+2)))
						box.tag_config('hclasses', foreground='purple')
						#navigation.netwidgets(box, count)				   

					elif '\telse' in str(item) or '\tif' in str(item) or '\telif' in str(item) or 'finally' in str(item) and ':' in str(item) and check == 'block':
						box.insert('end', str(item))
						box.tag_add('cflow', str(float(count+1)), str(float(count+2)))
						box.tag_config('cflow', foreground='brown')
					else:
						#box.tag_add('start', '1.0', 'end')
						#box.tag_config('start', background='red')
						box.insert('end', str(item))
						

						
											

				   
			
			
			controlers.sessionmanager(currentdir=directory, recentfiles=directory, query=False)
			#controlers.sessionmanager(recentfiles=directory, query=False)
			print(directory)
			print('whats added?')
			tsearch = directory.replace('py', 'txt')
			print(tsearch)
			if os.path.isfile(tsearch) == True:
				notes.delete('1.0', 'end')
				with open(tsearch, 'r') as textFiles:
					for item in textFiles:
						
						notes.insert('end', item)
			
			#controlers.shiftpage(navigation.secondpage(directory=directory))
	#----------------------------------run command-------------------
	def runfile(self, output):
		directory = controlers.sessionmanager(currentdir='Query', query=True)
		
		if directory == None:
			messagebox.showinfo('choose a path', 'You need to save before you run')
		else:
			controlers.savefile(self, output, directory=directory)
			new = str(directory).replace('C:', '')
			sts = os.system('python' + str(new))
		#exec(open(str(navigation.directory)).read())
		#savefile(directory, output)
	#---------------------------quick save/ save commands------------------
	def savefile(self, output, directory):
		print('check' + str(directory))
		#newdir = controlers.sessionmanager(currentdir='query', query=True)
		if '.py' in str(directory):
			controlers.sessionmanager(currentdir=directory, query=False)
			#directory=controlers.sessionmanager(currentdir='Query', query='True')
		if directory == None:
			messagebox.showinfo('Save?', 'You need to specify a filename. Choose a directory')
			print('You need to specify a filename. Choose a directory')
			
		else:
			print(directory)
			
			
			with open(str(directory), 'w') as file:
				file.write(str(output))

	
		#controlers.refreshpage(self, directory=directory, function=navigation.secondpage)
	def refreshpage(self, directory, function):
		#frame = tkinter.Frame(self)
		
		#self.destroy()
		print('hi')
		function(directory)
		controlers.goaway(self)
		
	#-----------------------------------hardly used screen controler/ shiftpage and goaway--------------
	def shiftpage(self, frame, function):
		#frame = tkinter.Frame(self)
		
		#self.destroy()
		print('hi')
		function()
		controlers.goaway(self)
			
	'''def waiting(self, frame):
		 h = lambda: main.shiftpage(self, frame)
		 self.after(3000, lambda: h())'''

	def goaway(self):
		self.withdraw()

	#--------------------------search function functions-----------------
	def searched(widget=None, editor=None, butts=None, linelabel=None):
	 
		results = widget.get()
		directory = controlers.sessionmanager(currentdir='Query', query=True)
		print(directory)
		print(results)
		counts = []
		
		with open(str(directory), 'r') as file:
			for count, item in enumerate(file):

				if str(results) in item:
					print(str(results))

					print(count)
					counts += [count]
						
					print(counts)


		
		
		translatestring = str(counts)[1:-1]
		linelabel['text'] = translatestring
		controlers.textfocus(butts=butts, *counts, editor=editor)
	def textfocus(*counts, editor=None, butts):
	 
		if int(butts.get()) >= len(counts):
			editor.tag_remove('highlight', '1.0', 'end')
			h=counts[0]
		
		else:

			print(counts)
			h = counts[int(butts.get())]
			count = str(h)
			count2 = int(counts[int(butts.get())]) + 2
			count2 = str(count2)
			print('check' + str(count2))
			editor.see(count+ '.0')
			editor.tag_add('highlight', count + '.0', count2+'.0')
			editor.tag_configure('highlight', background='yellow')
			editor.focus_set()
			editor.mark_set('insert', count+'.0')
		
	
class navigation(tkinter.Tk):
	def __init__(self):
		tkinter.Tk.__init__(self)
		navigation.secondpage(self)
	

		
	#------------------------main editor window widget----------------------
	def secondpage(self, directory=None):
		controlers.sessionmanager(currentdir='none')
		print(directory)
		s = Style()
		s.theme_use('clam')
		newdirectory = controlers.sessionmanager(currentdir='Query', query='True')
		print('im always angry')
		self.geometry('850x850+450+50')
		self.winfo_toplevel().title('wincode')
		recentfiles = controlers.sessionmanager(recentfiles='Query', query=True)
		print(recentfiles)
		frames = tkinter.Frame(self)
		#self.attributes("-fullscreen", True)
		frames.grid(sticky='e')
		#frames.pack(side='bottom')
		#-------------------------------editor and text boxes---------------

		t = lambda: main.otherpage(self, frames)
	   
		
		filetitles = tkinter.Label(frames, text='unsaved')

		filetitles.grid(row=0, column=3, pady=20, sticky='n')


		

		#grid(row=0, column=3, pady=20, sticky='n')
		#filetext.set('Unsaved File')
		editor = ScrolledText(frames, height=40)
		editor.grid(row=1, column=3, rowspan=25, pady=10)
		editor.config(wrap='none')

		scroll = tkinter.Scrollbar(frames, command=editor.xview, orient='horizontal')
		scroll.grid(row=38, column=3, sticky='nsew')
		editor['xscrollcommand'] = scroll.set
		#editor.config(tabs=('10m'))
		'''def tab(arg):
		    print("tab pressed")
		    editor.insert(tkinter.INSERT, " " * 4)

		editor.bind("<Tab>", tab)'''
		#editor.pack(side='bottom')
		Otext = tkinter.Text(frames, height=5)
		Otext.grid(row=40, column=3, sticky='s')
		outputes = lambda: editor.get("1.0",'end')
		notes = navigation.noteinterface(self, frames, editor)
		openfiles = lambda: controlers.openfiles(title=filetitles, notes=notes, box=editor, directory=str(filedialog.askopenfilename(initialdir = './', title='select file', filetypes=(('.py', '*.py'), ('.txt', '*.txt')))))
		#h = lambda: filedialog.askopenfilname(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
		allfiles = lambda: controlers.savefile(self=self, directory=filedialog.asksaveasfilename(initialdir = './', title ='title', defaultextension='.py', filetypes = (('py files', '*.py'), ('text', '*.txt'))), output=str(editor.get("1.0",'end')))
		navigation.netwidgets(self, frames)
		listbox = navigation.netwidgets(self, frames)
		saves = lambda: controlers.savefile(directory=str(allfiles), output=editor.get("1.0", 'end'))
		#-------------------------------menu---------------
		menubar = tkinter.Menu(self)
		editmenu = tkinter.Menu(menubar)
		menubar.add_cascade(label='file', menu=editmenu)
		editmenu.add_command(label='save as', command=allfiles)
		runfile = lambda: controlers.runfile(self, output=editor.get('1.0','end'))
		editmenu.add_command(label='run program', command=runfile)
		editmenu.add_command(label='open file', command=openfiles)
		searchbar = lambda: navigation.rightCWindow(None, editor) 
		editmenu.add_command(label='search file', command=searchbar)
		defaultsave = lambda: controlers.savefile(self=self, directory=controlers.sessionmanager(currentdir='Query', query=True), output=str(editor.get("1.0",'end')))
		menubar.add_command(label="save", command=defaultsave)
		# drop down for the file tab
		menubar.add_command(label="exit", command=self.destroy)
		self.config(menu=menubar)
		listmenu = tkinter.Menu(menubar)
		#for count, item in enumerate(recentfiles):
		#listmenu.add_command(label='Recent Files')
		editmenu.add_cascade(label='Recent Files', menu=listmenu)
		newfiles = []
		#editControls.startsthreads(editor)
		
		newbutt = tkinter.Button(frames, text='text', command=lambda:editControls.startsthreads(editor))
		newbutt.grid()
		#self.bind('<Return>', lambda event, widget=editor: editControls.startsthreads(event, widget))
		for item in recentfiles:
			navigation.functionscall(listmenu=listmenu, box=editor, directory=item[0], notes = notes, title=filetitles)
		
		s = Style()
		s.theme_use('clam')
		self.after(7000, lambda: navigation.testfunc(self, editor, listbox))
		
	#-------------------------call backs/event monitoring---------------

	def testfunc(self, editor, listbox):
		# class callback
		print('did callback fire')
		classIds = []
		methodIds = []
		allIds = []
		
		self.after(10000, lambda: navigation.waiting(self, editor, listbox))
				
		current_input = [editor.get('1.0', 'end').split('\n')]
		for item in current_input:
			for count, items in enumerate(item):
				if 'cla' + 's' * 2 + ' ' in str(items) and ':' in str(items):
					print(items)
					print(count)
					allIds.append(count)
					classIds.append(count)
					if str(items) not in listbox.get(0, 'end'):
						listbox.insert('end', str(items))
				if '	def ' in str(items) and ':' in str(items):
					print(items)
					print(count)
					allIds.append(count)
					methodIds.append(count)
					if str(items) not in listbox.get(0, 'end'):
						listbox.insert('end', str(items))
		
					
		for item in classIds:
			editor.tag_add('alter_class', float(item + 1), float(item + 2))
			editor.tag_configure('alter_class', foreground='purple')
			
		for item in methodIds:
			editor.tag_add('alter_method', float(item + 1), float(item + 2))
			editor.tag_configure('alter_method', foreground='blue')

		for count, item in enumerate(listbox.get(0, 'end')):
			#print(str(x) + 'integer')
			
			if 'class ' in str(item):
				listbox.itemconfig(count, {'foreground': 'red'})
			else:
				listbox.itemconfig(count, {'foreground': 'blue'})
			
		listbox.bind("<<ListboxSelect>>", lambda event=None, lists=listbox: navigation.lbox_output(event, lists, allIds, editor))
		
		
	def waiting(self, editor, listbox):
		print('waiting')
		self.after(5000, lambda: navigation.testfunc(self, editor, listbox))
		
			
		
		
	#-------------------------------side bar/peripherals---------------
	def functionscall(listmenu=None, box=None, notes=None, directory=None, title=None):
		#temporary function to get lambda to work in for loop
		h = lambda:controlers.openfiles(box=box, notes=notes, directory=directory, title=title)
		listmenu.add_command(label=directory, command=h)
	#-----------------------------builds listbox on the sidebar-------------
	def netwidgets(self, frames):
		lists = tkinter.Listbox(frames)
		
						
		#lists.pack(side='right')
						
		lists.grid(row=3, column=4, pady=10)
		label = tkinter.Label(frames, text='add a url')
		label.grid(row=4, column=4)
		url = tkinter.Entry(frames)
		url.grid(row=2, column=4, pady=5)
		scroll = tkinter.Scrollbar(frames, command=lists.yview, orient='vertical')
		scroll.grid(row=3, column=6, sticky='ns')
		#lists.config(wrap='none')
		lists['yscrollcommand'] = scroll.set

		#url.pack(side='right')
		return lists
	def lbox_output(event, listbox, allIds=None, editor=None):
		print(listbox.get('active'))
		integer = (listbox.curselection())
		for item in integer:
			editor.see(str(float(allIds[item])))
		
		
	#-------------------------------notes---------------

	def noteinterface(self, frames, editor):
		notes = tkinter.Text(frames, width=15)
		notes.grid(row=6, column=4, sticky='s')
		newdirectory = controlers.sessionmanager(currentdir='Query', query=True)
		print('notes' + str(newdirectory))
	
		sendfile = lambda: controlers.savefile(self=self, output=notes.get('1.0', 'end'), directory=str(controlers.sessionmanager(currentdir='Query', query=True)).replace('py', 'txt'))
		submit = tkinter.Button(frames, width=15, text='submit', command=sendfile)
		submit.grid(row=7, column=4, sticky='s')

		#--------------Search-------------------------#
		
		#search = tkinter.Entry(frames)
		#search.grid(columns=5, rows=1, sticky='n')
		self.bind('<Control-f>', lambda event, widget=editor: navigation.rightCWindow(event, widget))
		self.bind('<Button-3>', lambda event, cords=self, widget=editor: editControls(event, cords, editor=widget))
		return notes

	def rightCWindow(shit, editor, count=0):
		#---------search function-------------
		count = 0
		framess = Toplevel()
		#framess = tkinter.Frame(popup)
		
		searchbox = tkinter.Entry(framess)
		searchbox.grid()
		
		#check = tkinter.Frame(popup)
		
		tkinter.intvar = count
		
		linelabel = tkinter.Label(framess, text='Navigate with index from index')
		linelabel.grid()
		nelabel = tkinter.Label(framess, text='Find Text')
		nelabel.grid()
		Cvalue = tkinter.Entry(framess)
		Cvalue.focus()
		Cvalue.grid()
		framess.after(500, lambda: framess.focus_force())
		searchbox.after(700, lambda: searchbox.focus_force())
		Cvalue.insert('end', str(count))
		label = tkinter.Label(framess, text='jump to line')
		label.grid()
		thecount = lambda: navigation.count(Cvalue)
		butts2 = tkinter.Button(framess, foreground='blue', text='+', command=thecount)
		
		butts2.grid()
		tempfunc = lambda: controlers.searched(widget=searchbox, editor=editor, butts=Cvalue, linelabel=linelabel)
		butts = tkinter.Button(framess, foreground='blue', text='search', width=40, command=tempfunc)

		butts.grid()
		
		
		removeit = lambda: editor.tag_remove('highlight', '1.0', 'end')
		clearbutts = tkinter.Button(framess, width=40, foreground='blue', text='clear', command=removeit)
		clearbutts.grid()
		
		#------------------search function indexs return items-----------
		#referenced above
	def newfuncs(notes=None, box=None, title=None, directory=None):
		return controlers.openfiles(box=box, notes=notes, title=title, directory=directory)
		
	def count(Cvalue):
		newval = int(Cvalue.get())
		Cvalue.delete(0, 'end')
		Cvalue.insert('end', str(newval + 1))
		#print(newval)

	def tagremover():
		
		controlers.textfocus(remove=True)
		#-------------------------cut/copy/paste---------------------
class editControls(object):
	editor = 0
	def __init__(self, event, cords, editor):
		frame = Toplevel()
		xcord = cords.winfo_pointerx()
		ycord = cords.winfo_pointery()
		print(xcord)
		print(ycord)
		but_width = 20
		string_value = f'75x75+{xcord}+{ycord}'
		frame.geometry(string_value)
		buttoncopy = lambda: editControls.copy(self, editor, frame)
		copy_button = tkinter.Button(frame, text='Copy', command=buttoncopy, width=but_width, anchor='w')
		copy_button.grid()

		button_cut = lambda: editControls.cut(self, editor, frame)
		cut_button = tkinter.Button(frame, text='Cut', command=button_cut, width=but_width, anchor='w')
		cut_button.grid()

		button_paste = lambda: editControls.paste(self, editor, frame)
		paste_button = tkinter.Button(frame, text='Pste', command=button_paste, width=but_width, anchor='w')
		paste_button.grid()

	def copy(self, editor, frame):
		print('check')
		#frame.clipboard_append('shit')
		editor.focus_set()
		editor.event_generate('<<Copy>>')
		
		print(frame.clipboard_get())
		
	def cut(self, editor, frame):
		print('check')
		#frame.clipboard_append('shit')
		editor.focus_set()
		editor.event_generate('<<Cut>>')
		
		print(frame.clipboard_get())
	def paste(self, editor, frame):
		print('check')
		#frame.clipboard_append('shit')
		editor.focus_set()
		editor.event_generate('<<Paste>>')
		
		print(frame.clipboard_get())


	'''def startsthreads(editor):
		q = Queue(maxsize=0)
		r = Queue(maxsize=0)
		for item in range(10):
			r.put(editor)
		#q.put(editor)
		fake = 0
		proc = []
		#shitfuck = editControls.prints_numbers(editor)
		for item in range(10):
			q.put(editor)
			
	
		refresh = Thread(target=editControls.shortcuts, args=(editControls.prints_numbers, q))
		
		refresh.start()
		
			

	def class_shortcut(value, editor):
		for item in value:
			item.join()
		
	
	def shortcuts(shitfuck, value):
		#self= Toplevel()
		for x in range(10):
			print('checking')
		
					
		
			time.sleep(10)
			shitfuck(q)
		
		
	
		
		
	def prints_numbers(editor):
		print('god damnit mother fucker')
		print(editor.get('1.0', 'end'))
		#editControls.startsthreads(editor)
		
	def basic_queues(editor):
		pass
		

	def do_stuff(q):
		while True:
			print(q.get())
			q.task_done()'''





main2 = main()
#classtwo = editControls
#classtwo()
main2.mainloop()

























































































































































































































































































































































































































































































































































































































































































































































