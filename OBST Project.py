from tkinter import *
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
import string


class Node:
    def __init__(self, data, s):
        self.data = data
        self.left = None
        self.right = None
        self.st = s

    def show(self):
        print(str(self.data), self.st, "\t")


class Node2:
    def __init__(self, c, s, c2):
        self.left = None
        self.right = None
        self.cost = c
        self.name = s
        self.cost2 = c2


def height(r):
    # Function to calculate height of tree
    if r is None:
        return -1
    elif (r.left is None) and (r.right is None):
        return 0
    else:
        leftheight = height(r.left)
        rightheight = height(r.right)
        if leftheight > rightheight:
            return leftheight + 1
        else:
            return rightheight + 1


def nodes_level(r, level, lis):
    # Appending the Nodes at same level in List "lis"
    if r is None:
        return
    elif level == 0:
        lis.append(r.data)
    nodes_level(r.left, level - 1, lis)
    nodes_level(r.right, level - 1, lis)


def level_o(r):
    # Fuction to return a list "lis" that contains Level-wise Nodes
    level = 0
    lis = []
    hgt = height(r)
    while level <= hgt:
        nodes_level(r, level, lis)
        level = level + 1
    return lis


def construct_tree(r1, start, end, root, list1, s):
    # This Function returns the Root Node of the finally constructed Tree and
    # Prints the Nodes on the Console in Level-order fashion
    if start < end:
        r1 = Node(list1[root[start][end]], s)
        r1.show()
        r1.left = construct_tree(r1.left, start, root[start][end] - 1, root, list1, s + "L")
        r1.right = construct_tree(r1.right, root[start][end] + 1, end, root, list1, s + "R")
    elif start == end:
        r1 = Node(list1[root[start][end]], s)
        r1.show()
    return r1


class OBST:
    # This class creates another window which is used to display the finally formed Tree
    # And contains a search area which returns the cost for searching the the text for that particular word
    def __init__(self, array):
        # This function is started as soon as an object of OBST class is created.
        # It creates a new window with canvas on it to display the OBSTree.
        # This window has two buttons : Search Button and Exit Button
        self.outlineColor = '#1e1e1e'
        self.mainScreenColor = '#e6e6e6'
        self.menuBarColor = '#34495e'
        self.nodeColor = '#32e632'
        self.buttonColor = '#1abc9c'

        self.canvasHeight = 600
        self.canvasWidth = 1200

        self.window = Tk()
        self.window.title('OBST')

        self.window.geometry(f"{self.canvasWidth}x{self.canvasHeight}")
        self.exitButton = Button(self.window, width=10, font=('arial', 8), text='Exit', borderwidth=0,
                                 command=self.exit)
        self.canvas = Canvas(self.window, height=self.canvasHeight - 80, width=self.canvasWidth, borderwidth=0,
                             highlightthickness=0)
        self.searchEntry = Entry(self.window, width=25, borderwidth=0, justify=CENTER, font=('arial', 8))
        self.searchButton = Button(self.window, width=10, font=('arial', 10), text='Search', borderwidth=0,
                                   command=lambda: self.searchKey())
        self.setColorScheme()
        self.canvas.pack(side='bottom')
        self.searchButton.place(x=300, y=20)
        self.exitButton.place(x=1000, y=30)
        self.nodeWidth = 30
        self.searchEntry.place(x=300, y=48)

        self.l = array
        self.name = ""
        self.cost = 0
        self.cost2 = 0
        self.adding = False
        self.loopActive = True
        self.root = None
        self.n = 0
        self.nline = 0
        self.disptree = Button(self.window, width=10, font=('arial', 10), text='Search', borderwidth=0, command=self.UI())
        self.UI()

    def search(self, rt, key, cst, level):
        # This Function displays if the Search Key was found or not and the Cost
        # required for the Search operation
        if rt.name == key:
            s = str(rt.name + " found and the cost is " + str(cst + rt.cost * level))
            self.canvas.create_text(150, 30 + self.nline, text=str(s), fill='black', font=('arial', 10, 'bold'))
            self.nline += 15
        else:
            if len(key) < len(rt.name):
                if rt.left is None:
                    s = key + " was not found and the cost is " + str(cst + rt.cost2 * (level + 1))
                    self.canvas.create_text(150, 30 + self.nline, text=str(s), fill='black', font=('arial', 10, 'bold'))
                    self.nline += 15
                else:
                    self.search(rt.left, key, cst + rt.cost * level, level + 1)
            elif len(key) > len(rt.name):
                if rt.right is None:
                    s = key + " was not found and the cost is " + str(cst + rt.cost2 * (level + 1))
                    self.canvas.create_text(150, 30 + self.nline, text=str(s), fill='black', font=('arial', 10, 'bold'))
                    self.nline += 15
                else:
                    self.search(rt.right, key, cst + rt.cost * level, level + 1)
            else:
                if key < rt.name:
                    if rt.left is None:
                        s = key + " was not found and the cost is " + str(cst + rt.cost2 * (level + 1))
                        self.canvas.create_text(150, 30 + self.nline, text=str(s), fill='black',
                                                font=('arial', 10, 'bold'))
                        self.nline += 15
                    else:
                        self.search(rt.left, key, cst + rt.cost * level, level + 1)
                else:
                    if rt.right is None:
                        s = key + " was not found and the cost is " + str(cst + rt.cost2 * (level + 1))
                        self.canvas.create_text(150, 30 + self.nline, text=str(s), fill='black',
                                                font=('arial', 10, 'bold'))
                        self.nline += 15
                    else:
                        self.search(rt.right, key, cst + rt.cost * level, level + 1)

    def searchKey(self):
        # This Function takes the Search Key value from the Textbox if its length is not 0
        if len(self.searchEntry.get()) == 0:
            self.n = 0
        else:
            self.search(self.root, self.searchEntry.get(), 0, 0)

    def exit(self):
        # This Function is used to set the loopActive value to False
        # which was used to update the window continuously for any changes
        # and then destroys the window
        self.loopActive = False

    def setColorScheme(self):
        # This Function is used to set the colour scheme for the different elements
        # on the window screen
        self.outlineColor = '#1e1e1e'
        self.mainScreenColor = '#e6e6e6'
        self.menuBarColor = '#34495e'
        self.nodeColor = '#32e632'
        self.buttonColor = '#1abc9c'

        self.searchEntry.configure(bg=self.mainScreenColor, fg=self.outlineColor, insertbackground=self.outlineColor)
        self.window.configure(bg=self.menuBarColor)
        self.canvas.configure(bg=self.mainScreenColor)

    def addEntry(self, w):
        # This Function is used to add new Nodes to the Tree
        self.adding = True
        self.name = w[0]
        self.cost = w[2]
        self.cost2 = w[3]
        self.n = 1

    def createNode(self, n, c, c2):
        # This Function creates new Nodes
        temp = Node2(c, n, c2)
        return temp

    def insert(self, subRoot, n, c, c2):
        # This is a Recursive Function used to insert and display new Nodes on the Window canvas
        if subRoot is None:
            return self.createNode(n, c, c2)
        elif len(n) < len(subRoot.name):
            subRoot.left = self.insert(subRoot.left, n, c, c2)
        elif len(n) == len(subRoot.name):
            if n < subRoot.name:
                subRoot.left = self.insert(subRoot.left, n, c, c2)
            else:
                subRoot.right = self.insert(subRoot.right, n, c, c2)
        else:
            subRoot.right = self.insert(subRoot.right, n, c, c2)

        return subRoot

    def UI(self):
        # This Function is used to update the window continuously for any changes if made
        # And displaying the Tree on the Canvas
        i = 0
        while self.loopActive:
            self.canvas.update()
            if i < len(self.l):
                self.addEntry(self.l[i])
                i += 1
            if self.n == 0:
                self.inorder(self.root, 30, 600, 300)
            if self.adding:
                self.root = self.insert(self.root, self.name, self.cost, self.cost2)
                self.adding = False
            self.n = 0
            self.inorder(self.root, 30, 600, 300)
        self.window.destroy()

    def inorder(self, subRoot, row, col, sep):
        # This is a Recursive Function used to display the Tree on the Canvas properly
        if subRoot:
            if subRoot.right is not None:
                self.canvas.create_line(col, row, col + sep, row + 50, width=2, fill=self.outlineColor)
            if subRoot.left is not None:
                self.canvas.create_line(col, row, col - sep, row + 50, width=2, fill=self.outlineColor)

            self.inorder(subRoot.left, row + 50, col - sep, sep / 2)

            # print(subRoot.data, end=" ")
            self.canvas.create_oval(col - self.nodeWidth / 2, row - self.nodeWidth / 2, col + self.nodeWidth / 2, row + self.nodeWidth / 2, fill=self.nodeColor, outline=self.outlineColor, width=2)
            self.canvas.create_text(col, row, text=str(subRoot.name), fill='black', font=('arial', 10, 'bold'))

            self.inorder(subRoot.right, row + 50, col + sep, sep / 2)


def getwordlist(file_list, n):
    # This Function creates a new File which stores all the contents of the user's data
    # It uses the NLTK module to segregate different words and remove Punctuations and
    # Stop-words from the data and finally retuns a list of disticnt words along with their
    # frequencies, probabilities of finding them and their unsuccessfull probabilities
    file_text = []
    f = open("Test.txt", "w")
    f.write("")
    f.close()
    f = open("Test.txt", "a+")
    for f2 in file_list:
        f1 = open(f2)
        file_text.append(f1.read())
        f1.seek(0)
        f.write(f1.read())
        f.write("\n")
    f.close()
    f = open("Test.txt")
    default_stopwords = set(stopwords.words('english'))
    punc_stopwords = set(string.punctuation)
    punc = {"''", "``"}
    all_stopwords = default_stopwords | punc_stopwords | punc
    f.seek(0)
    words = word_tokenize(f.read())
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    words = [word for word in words if word.lower() not in all_stopwords]
    fdist = FreqDist(words)
    word_list = []
    for word, frequency in fdist.most_common(n):
        word_list.append([word, frequency, round(frequency / len(words), 2)])
    for w in word_list:
        u = 0
        for i in file_text:
            if w[0] not in i:
                u += 1
        w.append(round(u / len(file_list), 2))
    x = 0
    for i in word_list:
        x += i[2]
    word_list = [["unsuccesful", 0, 0, 1 - x]] + word_list
    return word_list


def printlist(word_list):
    # This Function displays the Word list on the Main Window and returns the
    # Wordlist after sorting it according to the length of the words.
    rowvar = 2
    colvar = 0
    temp = word_list[0]
    word_list.pop(0)
    word_list.sort(key=lambda x: len(x[0]))
    word_list = [temp] + word_list
    print("Word\t\tFrequency\t\tProbability\t\tUnsuccessful Prob")
    rowvar += 1
    Label(groot, text="word", bg=themecolor).grid(row=rowvar, column=colvar)
    colvar += 1

    Label(groot, text="frequency", bg=themecolor).grid(row=rowvar, column=colvar)
    colvar += 1

    Label(groot, text="probability", bg=themecolor).grid(row=rowvar, column=colvar)
    colvar += 1

    Label(groot, text="Unsuccessful Prob", bg=themecolor).grid(row=rowvar, column=colvar)
    rowvar += 1

    for w in word_list:
        colvar = 0
        print(w[0], "\t\t", w[1], "\t\t", w[2], "\t\t", w[3])
        Label(groot, text=w[0], bg=themecolor).grid(row=rowvar, column=colvar + 0)
        Label(groot, text=w[1], bg=themecolor).grid(row=rowvar, column=colvar + 1)
        Label(groot, text=w[2], bg=themecolor).grid(row=rowvar, column=colvar + 2)
        Label(groot, text=w[3], bg=themecolor).grid(row=rowvar, column=colvar + 3)

        rowvar += 1
    print("\n")

    return word_list


def dis(mat, rowvar, colvar):
    # This Function is used to display a matrix on the Main Window
    k = 0
    for i in mat:
        if len(i) != 0:
            s = ""
            for j in i:
                s = s + str(j) + "\t"
            Label(groot, text=s, bg=themecolor).grid(row=rowvar, column=colvar)
            rowvar += 1


def dispmat(l, rowvar, colvar):
    # This Function creates and displays three matrices used to create an OBST, which are
    # Weight Matrix, Evolution Matrix and Root Matrix on the Main Window. Finally the
    # Root Matrix is returned
    s = []
    for i in range(len(l)):
        s.append(round(l[i][2] + l[i][3], 2))
    weight = [[]]
    evolution = [[]]
    root = [[]]
    for i in range(len(l)):
        weight.append([-99] * len(l))
        evolution.append([99] * len(l))
        root.append([99] * len(l))
    for i in range(1, len(l) + 1):
        weight[i][i - 1] = l[i - 1][3]
        evolution[i][i - 1] = l[i - 1][3]
    for k in range(1, len(l)):
        for i in range(1, len(l) - k + 1):
            j = i + k - 1
            evolution[i][j] = 99
            weight[i][j] = round(weight[i][j - 1] + s[j], 2)
            for r in range(i, j + 1):
                t = evolution[i][r - 1] + evolution[r + 1][j] + weight[i][j]
                if t < evolution[i][j]:
                    evolution[i][j] = round(t, 2)
                    root[i][j] = r
    # colvar=0
    x = rowvar
    Label(groot, text="weight", bg=themecolor).grid(row=x, column=colvar)
    dis(weight, rowvar + 1, colvar)
    Label(groot, text=" ", bg=themecolor).grid(row=x, column=colvar + 1)
    Label(groot, text="evolution", bg=themecolor).grid(row=x, column=colvar + 2)
    dis(evolution, rowvar + 1, colvar + 2)
    Label(groot, text=" ", bg=themecolor).grid(row=x, column=colvar + 3)
    return root


def clickbutt1():
    # This Function is initiated as soon as the Submit Button is clicked on the Main Window
    # It takes the files from which the data is to be extracted and the number of nodes
    # to be worked upon from the User and passes it to the "getwordlist" function which
    # returns the wordlist which in turn is passed on to the "printlist" function that
    # returns the final wordlist to be used while constructing OBST. The wordlist in the
    # form of "word_list" is passed on to "dispmat" function that returns the Root matrix
    # which is stored as "root_mat" and passed on to the "contruct_tree" function which
    # forms the OBST tree and returns the root node. This function also generates a new
    # Button which is used to display the finally formed Tree. It returns the wordlist.
    n = int(e1.get())
    file_list = e2.get().split(",")
    # print(file_list,n)
    word_list = getwordlist(file_list, n)
    word_list = printlist(word_list)
    Label(groot, text=" ", bg=themecolor).grid(row=rowvar + n + 3, column=colvar)
    root_mat = dispmat(word_list, rowvar + n + 4, 0)
    tree_root = None
    tree_root = construct_tree(tree_root, 1, n, root_mat, word_list, "")
    button3 = Button(groot, text="Print tree", command=lambda: OBST(level_o(tree_root)), bg=buttoncolor, fg='white').grid(row=1, column=colvar + 3)
    # OBST(level_o(tree_root))
    return word_list


# Main Code
# A new Window is created using Tkinter as "groot"
# It has two Text Fields for the user to enter the list of Files for the
# text to be extracted from and the number of Nodes to be worked upon.
# Both the user inputs are sent for processing using the "Submit" Button
# and initiates the "clickbutt1" Function. And the "Exit" Button is
# used to exit from the code.

themecolor = '#C8C8C8'
buttoncolor = '#404040'
groot = Tk()
w, h = groot.winfo_screenwidth(), groot.winfo_screenheight()
groot.geometry("%dx%d+0+0" % (w, h))
groot.configure(bg=themecolor)

rowvar = 0
colvar = 0

e1 = Entry(groot, width=30, fg="black", borderwidth=5)
e2 = Entry(groot, width=30, fg="black", borderwidth=5)
butt1 = Button(groot, text="Submit", command=clickbutt1, bg=buttoncolor, fg='white')
button2 = Button(groot, text="Exit", command=lambda: groot.destroy(), bg=buttoncolor, fg='white')

Label(groot, text="Enter no of nodes and file list.", bg=themecolor, fg="black").grid(row=rowvar, column=colvar)
rowvar += 1
e1.grid(row=rowvar, column=colvar)
e2.grid(row=rowvar, column=colvar + 1)
butt1.grid(row=rowvar, column=colvar + 2)
button2.grid(row=rowvar, column=colvar + 4)
rowvar += 1

groot.mainloop()