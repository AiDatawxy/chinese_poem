############################################################
''' 3 '''

class FrameDynasty(Frame):
	''' 显示朝代的 Frame '''

	def __init__(self, parent, frame_author):
		super().__init__(parent)

		self.dynasty_choose = ''
		self.frame_author = frame_author

		self.frame_showDynasty = Frame(self)
		self.frame_showDynasty.pack()

		self.lb_dynasty = Listbox(self.frame_showDynasty, height=35)
		self.sb_dynasty = Scrollbar(self.frame_showDynasty)
		self.lb_dynasty.config(yscrollcommand=self.sb_dynasty.set)
		self.sb_dynasty.config(command=self.lb_dynasty.yview)
		self.f_showDynasty()
		self.lb_dynasty.pack(side=LEFT, fill=Y)
		self.sb_dynasty.pack(side=LEFT, fill=Y)

		self.bt_dynasty = Button(self, text='确定朝代', command=self.f_bt_dynasty)
		self.bt_dynasty.pack()


	def f_showDynasty(self):
		for dynasty in dynasty_authors.keys():
			self.lb_dynasty.insert('end', dynasty)


	def f_bt_dynasty(self):
		if self.lb_dynasty.curselection():
			self.f_setDynasty(self.lb_dynasty.get(self.lb_dynasty.curselection()))
			self.frame_author.f_setDynasty(self.f_getDynastyChoose())
			self.frame_author.f_showAuthor()
			self.frame_author.f_clearPoem()


	def f_getDynastyChoose(self):
		return self.dynasty_choose


	def f_setDynasty(self, dynasty):
		self.dynasty_choose = dynasty



class FrameAuthor(Frame):
	''' 显示诗人的 Frame '''

	def __init__(self, parent, frame_poem):
		super().__init__(parent)

		self.dynasty_choose = ''
		self.author_choose = ''
		self.frame_poem = frame_poem

		self.frame_showAuthor = Frame(self)
		self.frame_showAuthor.pack()

		self.lb_author = Listbox(self.frame_showAuthor, height=35)
		self.sb_author = Scrollbar(self.frame_showAuthor)
		self.lb_author.config(yscrollcommand=self.sb_author.set)
		self.sb_author.config(command=self.lb_author.yview)
		self.f_showAuthor()
		self.lb_author.pack(side=LEFT, fill=Y)
		self.sb_author.pack(side=LEFT, fill=Y)

		self.bt_author = Button(self, text='确定诗人', command=self.f_bt_author)
		self.bt_author.pack()


	def f_showAuthor(self, authors=None, mode='choose'):
		if mode == 'choose' and self.f_getDynastyChoose() != '':
			self.lb_author.delete(0, 'end')
			authors = [author for author in dynasty_authors[self.dynasty_choose]]
			authors = sorted(authors, key=lambda x: x.encode('utf-8'))
			for author in authors:
				self.lb_author.insert('end', author)
		elif mode == 'search':
			self.lb_author.delete(0, 'end')
			self.frame_poem.f_clearPoem()
			for author in authors:
				self.lb_author.insert('end', author)


	def f_bt_author(self):
		if self.lb_author.curselection():
			author = self.lb_author.get(self.lb_author.curselection())
			if '@' in author:
				self.f_setDynasty(author.split('@')[1])
				self.f_setAuthor(author.split('@')[0])
			else:
				self.f_setDynasty(self.f_getDynastyChoose())
				self.f_setAuthor(author)
			self.frame_poem.f_setDynasty(self.f_getDynastyChoose())
			self.frame_poem.f_setAuthor(self.f_getAuthorChoose())
			self.frame_poem.f_showPoem()


	def f_getDynastyChoose(self):
		return self.dynasty_choose


	def f_getAuthorChoose(self):
		return self.author_choose


	def f_setDynasty(self, dynasty):
		self.dynasty_choose = dynasty


	def f_setAuthor(self, author):
		self.author_choose = author


	def f_clearAuthor(self):
		self.f_setDynasty('')
		self.f_setAuthor('')
		self.lb_author.delete(0, 'end')


	def f_clearPoem(self):
		self.frame_poem.f_clearPoem()



class FramePoem(Frame):
	''' 显示诗词的 Frame '''

	def __init__(self, parent):
		super().__init__(parent)

		self.dynasty_choose = ''
		self.author_choose = ''
		self.poem_choose = ''

		self.frame_showPoem = Frame(self)
		self.frame_showPoem.pack()

		self.lb_poem = Listbox(self.frame_showPoem, height=35)
		self.sb_poem = Scrollbar(self.frame_showPoem)
		self.lb_poem.config(yscrollcommand=self.sb_poem.set)
		self.sb_poem.config(command=self.lb_poem.yview)
		self.f_showPoem()
		self.lb_poem.pack(side=LEFT, fill=Y)
		self.sb_poem.pack(side=LEFT, fill=Y)

		self.bt_poem = Button(self, text='确定诗词', command=self.f_bt_poem)
		self.bt_poem.pack()


	def f_showPoem(self, poems=None, mode='choose'):
		if mode == 'choose' and self.f_getDynastyChoose() != '' and self.f_getAuthorChoose != '':
			self.lb_poem.delete(0, 'end')
			poems = [poem for poem in author_poems[self.author_choose + '@' + self.dynasty_choose]]
			poems = sorted(poems, key=lambda x: x.encode('utf-8'))
			for poem in poems:
				self.lb_poem.insert('end', poem)
		elif mode == 'search':
			self.lb_poem.delete(0, 'end')
			for poem in poems:
				self.lb_poem.insert('end', poem)


	def f_bt_poem(self):
		if self.lb_poem.curselection():
			poem = self.lb_poem.get(self.lb_poem.curselection())
			if '@' in poem:
				self.f_setDynasty(poem.split('@')[1])
				self.f_setAuthor(poem.split('@')[0])
				self.f_setPoem(poem.split('@')[2])
			else:
				self.f_setPoem(poem)


	def f_getDynastyChoose(self):
		return self.dynasty_choose


	def f_getAuthorChoose(self):
		return self.author_choose


	def f_getPoemChoose(self):
		return self.poem_choose


	def f_setDynasty(self, dynasty):
		self.dynasty_choose = dynasty


	def f_setAuthor(self, author):
		self.author_choose = author


	def f_setPoem(self, poem):
		self.poem_choose = poem


	def f_clearPoem(self):
		self.f_setDynasty('')
		self.f_setAuthor('')
		self.f_setPoem('')
		self.lb_poem.delete(0, 'end')



class FrameSelect(Frame):
	''' 控制板块 '''

	def __init__(self, parent):
		super().__init__(parent)

		self.frame_search = Frame(self)
		self.frame_search.pack()
		self.lb_search = Label(self.frame_search, text='搜索诗人或诗词')
		self.lb_search.grid(row=1, column=1, sticky=W)
		self.var_search = StringVar()
		self.entry_search = Entry(self.frame_search, textvariable=self.var_search)
		self.entry_search.grid(row=1, column=2, columnspan=3, sticky=W)
		self.bt_search = Button(self.frame_search, text='搜索一下', command=self.f_bt_search)
		self.bt_search.grid(row=1, column=5)

		self.frame_showSearch = Frame(self)
		self.frame_showSearch.pack()
		self.frame_poem = FramePoem(self.frame_showSearch)
		self.frame_author = FrameAuthor(self.frame_showSearch, self.frame_poem)
		self.frame_dynasty = FrameDynasty(self.frame_showSearch, self.frame_author)
		self.frame_dynasty.pack(side=LEFT, fill=Y)
		self.frame_author.pack(side=LEFT, fill=Y)
		self.frame_poem.pack(side=LEFT, fill=Y)
		

	def f_bt_search(self):
		search =  self.var_search.get().strip()
		authors = []
		poems = []
		# 先看有没有这个诗人
		for dynasty in dynasty_authors.keys():
		    if search in dynasty_authors[dynasty]:
		        authors.append(search + '@' + dynasty)
		# 有这个诗人
		if len(authors) > 0:
			authors = sorted(authors, key=lambda x: x.encode('utf-8'))
			self.frame_author.f_showAuthor(authors, 'search')
		# 没有这个诗人，再看是不是诗词标题
		else:
			for author in author_poems.keys():
				for poem in author_poems[author]:
					if search in poem:
						poems.append(author + '@' + poem)
			# 是诗词标题
			if len(poems) > 0:
				self.frame_author.f_clearAuthor()
				poems = sorted(poems, key=lambda x: x.encode('utf-8'))
				self.frame_poem.f_showPoem(poems, 'search')
			# 也不是标题
			else:
				messagebox.showinfo('showinfo', '没有找到【诗人】或【诗词标题】')


	def f_getDynasty(self):
		return self.frame_poem.f_getDynastyChoose()


	def f_getAuthor(self):
		return self.frame_poem.f_getAuthorChoose()


	def f_getPoem(self):
		return self.frame_poem.f_getPoemChoose()



class FrameShow(Frame):
	''' 诗人板块 '''

	def __init__(self, parent):
		super().__init__(parent)

		self.dynasty = ''
		self.author = ''
		self.poem = ''

		# 按钮
		self.frame_infoPlot = Frame(self)
		self.frame_infoPlot.pack()

		# 文字部分
		self.frame_info = Frame(self.frame_infoPlot)
		self.frame_info.pack(side=LEFT, fill=Y)

		self.var_basic = StringVar()
		self.mg_basic = Message(self.frame_info, textvariable=self.var_basic, width=200)
		self.mg_basic.pack()
		self.f_showBasic()

		self.stext_desc = scrolledtext.ScrolledText(self.frame_info, width=50, height=41, wrap=WORD)
		self.stext_desc.pack()
		self.f_showDesc()

		self.stext_word = scrolledtext.ScrolledText(self.frame_info, width=50, height=23, wrap=WORD)
		self.stext_word.pack()
		self.f_showWord()

		# 图片部分
		self.frame_plot = Frame(self.frame_infoPlot)
		self.frame_plot.pack(side=LEFT, fill=Y)

		self.frame_plotLocation = Frame(self.frame_plot)
		self.frame_plotLocation.pack()
		self.cv_location = Canvas(self.frame_plotLocation, width=634, height=634)
		self.cv_location.pack()
		self.img_locationRender = None
		self.f_plotLocation()

		self.frame_plotWordCloud = Frame(self.frame_plot)
		self.frame_plotWordCloud.pack()
		self.cv_wordCloud = Canvas(self.frame_plotWordCloud, width=634, height=300)
		self.cv_wordCloud.pack()
		self.img_wordCloudRender = None
		self.f_plotWordCloud()


	def f_showBasic(self):
		if self.f_getDynasty() != '' and self.f_getAuthor() != '':
			author_key = self.f_getAuthor() + '@' + self.f_getDynasty()
			self.var_basic.set(
				'诗人： ' + self.f_getAuthor() + '\n' + 
				'朝代： ' + self.f_getDynasty() + '\n' + 
				'诗人星数： ' + str(sta_author3[author_key]['a_author_star']) + '\n' +
				'诗词数： ' + str(sta_author3[author_key]['a_poem_num']) + '\n' +
				'诗词平均星数： ' + format(sta_author3[author_key]['a_poem_star'] / sta_author3[author_key]['a_poem_num'], '0.1f')
			)


	def f_showDesc(self):
		self.stext_desc.delete(1.0, 'end')
		if self.f_getDynasty() != '' and self.f_getAuthor() != '' and self.f_getAuthor() in author_desc.keys():
			self.stext_desc.insert('end', author_desc[self.f_getAuthor()][:min(1000, len(author_desc[self.f_getAuthor()]))])


	def f_showWord(self):
		self.stext_word.delete(1.0, 'end')
		if self.f_getDynasty() != '' and self.f_getAuthor() != '' and self.f_getPoem() != '':
			for key, value in db.items():
				if self.f_getDynasty() == key.split('-')[0] and self.f_getAuthor() == key.split('-')[1] and self.f_getPoem() in key.split('-')[2]:
					self.stext_word.insert('end', '标题： ' + value['title'] + '\n诗词星数： ' + str(value['star']) + '\n意境意象： ' + value['tags'])
					self.stext_word.insert('end', '\n\n\n')
					self.stext_word.insert('end', value['content'])


	def f_plotLocation(self):
		self.cv_location.delete(ALL)
		if self.f_getAuthor() in has_plotLocation:
			img_locationLoad = Image.open('result_plotLocation/{0}足迹图.png'.format(self.f_getAuthor()))
		else:
			img_locationLoad = Image.open('result_plotLocation/足迹图.png')
		img_locationLoad = img_locationLoad.resize((634, 634))
		self.img_locationRender = ImageTk.PhotoImage(img_locationLoad)
		self.cv_location.create_image(0, 0, image=self.img_locationRender, anchor='nw')


	def f_plotWordCloud(self):
		self.cv_wordCloud.delete(ALL)
		if self.f_getDynasty() != '' and self.f_getAuthor() != '':
			author_key = self.f_getAuthor() + '@' + self.f_getDynasty()
			img_wordCloudLoad = Image.open('result_plotWordCloud/{0}词云图.png'.format(author_key))
		else:
			img_wordCloudLoad = Image.open('result_plotWordCloud/词云图.png')	
		img_wordCloudLoad = img_wordCloudLoad.resize((634, 300))
		self.img_wordCloudRender = ImageTk.PhotoImage(img_wordCloudLoad)
		self.cv_wordCloud.create_image(0, 0, image=self.img_wordCloudRender, anchor='nw') 


	def f_getDynasty(self):
		return self.dynasty


	def f_getAuthor(self):
		return self.author


	def f_getPoem(self):
		return self.poem


	def f_setDynasty(self, dynasty):
		self.dynasty = dynasty


	def f_setAuthor(self, author):
		self.author = author


	def f_setPoem(self, poem):
		self.poem = poem



class FrameSimilar(Frame):
	''' 相关诗人板块 '''

	def __init__(self, parent):
		super().__init__(parent)

		self.dynasty = ''
		self.author = ''
		self.emb_result = []
		self.tag_result = []
		self.tags = {}
		self.words = []
		self.authors = []
		self.allow = False

		# 按钮
		self.scale = Scale(self, from_=0, to=100, orient='horizontal', tickinterval=5, length=1200)
		self.scale.pack()

		self.frame_disSim = Frame(self)
		self.frame_disSim.pack()

		# 距离
		self.frame_dis = Frame(self.frame_disSim)
		self.frame_dis.pack(side=LEFT, fill=Y)

		self.frame_dis_text = Frame(self.frame_dis)
		self.frame_dis_text.pack()

		self.stext_disAuthors = scrolledtext.ScrolledText(self.frame_dis_text, width=23, height=40, wrap=WORD)
		self.stext_disAuthors.pack(side=LEFT, fill=Y)
		self.f_disAuthors()

		self.stext_disTags = scrolledtext.ScrolledText(self.frame_dis_text, width=23, height=40, wrap=WORD)
		self.stext_disTags.pack(side=LEFT, fill=Y)
		self.f_disTags()

		self.stext_disWords = scrolledtext.ScrolledText(self.frame_dis_text, width=23, height=40, wrap=WORD)
		self.stext_disWords.pack(side=LEFT, fill=Y)
		self.f_disWords()

		self.frame_disPlot = Frame(self.frame_dis)
		self.frame_disPlot.pack()
		self.fig_dis = Figure(figsize=(4, 4), dpi=100)
		self.fig_dis_plot = self.fig_dis.add_subplot(111)
		self.canvas_dis = FigureCanvasTkAgg(self.fig_dis, self.frame_disPlot)
		self.canvas_dis.get_tk_widget().pack(side=TOP, expand=1)

		# 相似
		self.frame_sim = Frame(self.frame_disSim)
		self.frame_sim.pack(side=LEFT, fill=Y)

		self.frame_sim_text = Frame(self.frame_sim)
		self.frame_sim_text.pack()

		self.stext_simAuthors = scrolledtext.ScrolledText(self.frame_sim_text, width=23, height=40, wrap=WORD)
		self.stext_simAuthors.pack(side=LEFT, fill=Y)
		self.f_simAuthors()

		self.stext_simTags = scrolledtext.ScrolledText(self.frame_sim_text, width=23, height=40, wrap=WORD)
		self.stext_simTags.pack(side=LEFT, fill=Y)
		self.f_simTags()

		self.stext_simWords = scrolledtext.ScrolledText(self.frame_sim_text, width=23, height=40, wrap=WORD)
		self.stext_simWords.pack(side=LEFT, fill=Y)
		self.f_simWords()

		self.frame_simPlot = Frame(self.frame_sim)
		self.frame_simPlot.pack()
		self.fig_sim = Figure(figsize=(4, 4), dpi=100)
		self.fig_sim_plot = self.fig_sim.add_subplot(111)
		self.canvas_sim = FigureCanvasTkAgg(self.fig_sim, self.frame_simPlot)
		self.canvas_sim.get_tk_widget().pack(side=TOP, expand=1)


	def f_disAuthors(self):
		self.f_Authros(self.stext_disAuthors, 'dis')


	def f_disTags(self):
		self.f_Tags(self.stext_disTags, 'dis')


	def f_disWords(self):
		self.f_Words(self.stext_disWords, 'dis')


	def f_disPlot(self):
		self.f_Plot(self.canvas_dis, self.fig_dis_plot, 'dis')


	def f_simAuthors(self):
		self.f_Authros(self.stext_simAuthors, 'sim')


	def f_simTags(self):
		self.f_Tags(self.stext_simTags, 'sim')


	def f_simWords(self):
		self.f_Words(self.stext_simWords, 'sim')


	def f_simPlot(self):
		self.f_Plot(self.canvas_sim, self.fig_sim_plot, 'sim')


	def f_Authros(self, stext_Authors, mode):
		stext_Authors.delete(1.0, 'end')
		if mode == 'dis' and self.allow:
			stext_Authors.insert('end', '诗人\t\t距离\n\n')
			for author_dict in self.emb_result:
				stext_Authors.insert('end', list(author_dict.keys())[0] + '\t\t' + format(list(author_dict.values())[0], '0.5f') + '\n')
		elif mode == 'sim' and self.allow:
			stext_Authors.insert('end', '诗人\t\t相似度\n\n')
			for author_dict in self.tag_result:
				stext_Authors.insert('end', list(author_dict.keys())[0] + '\t\t' + format(list(author_dict.values())[0], '0.5f') + '\n')
		elif mode == 'dis':
			stext_Authors.insert('end', '诗人\t\t距离\n\n')
		elif mode == 'sim':
			stext_Authors.insert('end', '诗人\t\t相似度\n\n')


	def f_Tags(self, stext_Tags, mode):
		stext_Tags.delete(1.0, 'end')
		stext_Tags.insert('end', '意境意象\t\t诗词数\n\n')
		self.tags = {}
		if mode == 'dis' and self.allow:
			for author_dict in self.emb_result:
				for tag, tag_num in sta_author3[list(author_dict.keys())[0]]['a_tag'].items():
					if tag in self.tags:
						self.tags[tag] += tag_num
					else:
						self.tags[tag] = tag_num
			for tag, tag_num in sta_author3[self.f_getAuthor() + '@' + self.f_getDynasty()]['a_tag'].items():
				if tag in self.tags:
					self.tags[tag] += tag_num
				else:
					self.tags[tag] = tag_num
		elif mode == 'sim' and self.allow:
			for author_dict in self.tag_result:
				for tag, tag_num in sta_author3[list(author_dict.keys())[0]]['a_tag'].items():
					if tag in self.tags:
						self.tags[tag] += tag_num
					else:
						self.tags[tag] = tag_num
			for tag, tag_num in sta_author3[self.f_getAuthor() + '@' + self.f_getDynasty()]['a_tag'].items():
				if tag in self.tags:
					self.tags[tag] += tag_num
				else:
					self.tags[tag] = tag_num
		self.tags = dict(sorted(self.tags.items(), key=lambda x:x[1], reverse=True))
		count = 0
		for tag, tag_num in self.tags.items():
			stext_Tags.insert('end', tag + '\t\t' + str(tag_num) + '\n')
			count += 1
			if count > 30:
				break


	def f_Words(self, stext_Words, mode):
		stext_Words.delete(1.0, 'end')
		stext_Words.insert('end', '词\t\t词频\n\n')
		self.words = []
		if mode == 'dis' and self.allow:
			for author_dict in self.emb_result:
				for word in author_wordCount[list(author_dict.keys())[0]]:
					self.words.append(word)
			for word in author_wordCount[self.f_getAuthor() + '@' + self.f_getDynasty()]:
				self.words.append(word)
		elif mode == 'sim' and self.allow:
			for author_dict in self.tag_result:
				for word in author_wordCount[list(author_dict.keys())[0]]:
					self.words.append(word)
			for word in author_wordCount[self.f_getAuthor() + '@' + self.f_getDynasty()]:
				self.words.append(word)
		self.words = Counter(self.words)
		self.words = dict(sorted(self.words.items(), key=lambda x: x[1], reverse=True))
		count = 0
		for word, word_num in self.words.items():
			stext_Words.insert('end', word + '\t\t' + str(word_num) + '\n') 
			count += 1
			if count > 30:
				break


	def f_Plot(self, canvas, fig_plot, mode):
		fig_plot.clear()
		if self.allow:
			self.authors = [self.f_getAuthor() + '@' + self.f_getDynasty()]
		if mode == 'dis' and self.allow:
			for author_dict in self.emb_result:
				self.authors.append(list(author_dict.keys())[0])
		elif mode == 'sim' and self.allow:
			for author_dict in self.tag_result:
				self.authors.append(list(author_dict.keys())[0])
		author_embs = [embeddings[author2id[i]] for i in self.authors if self.allow]
		matplotlib.rcParams['axes.unicode_minus'] = False
		for i, author in enumerate(self.authors):
			x = author_embs[i][0]
			y = author_embs[i][1]
			fig_plot.scatter(x, y, s=10)
		for x, y in [(-70, 60), (-25, 30)]:
			fig_plot.scatter(x, y, s=1, c='#FFFFFF')
		canvas.draw()


	def f_getDynasty(self):
		return self.dynasty


	def f_getAuthor(self):
		return self.author


	def f_setDynasty(self, dynasty):
		self.dynasty = dynasty


	def f_setAuthor(self, author):
		self.author = author


	def f_calculate(self):
		if self.f_getAuthor() != '' and self.f_getDynasty() != '':
			self.emb_result, self.tag_result = get_similarAuthors(self.f_getAuthor() + '@' + self.f_getDynasty(), self.scale.get())
			self.allow = True 
		else:
			self.allow = False

