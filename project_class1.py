from tkinter import Tk,Label,Frame,Button,Entry,messagebox,ttk,simpledialog #Tk is main window class
#Label to display text, Frame to hold widgets, Button for click, 
#messagebox to show pop-up messages.
from tkinter.ttk import Combobox  #Combobox is dropdown list to select options.
import time #module dealing with time functions.
from PIL import Image,ImageTk   #Image library in python.
import auto_creation   #import the module to ensure tables are created when program starts.
import sqlite3      #import database library to establish connections with databases.
import random       #import random module for first time password generation.
import gmail        #import gmail module to send emails to users.
import re           #import re module to check validation using regex expressions.

win = Tk() #main window of application.
win.title('My Project') #Main heading on window.
win.state('zoomed') #ensures full screen window.
win.resizable(width=False,height=False) #prevents resizing of window.
win.configure(background='#F7CAC9') #sets the background color to 'Azalea'. 

header_title = Label(win,text="Banking Automation",font=('Lucida Calligraphy',50,'bold'),background='#F7CAC9')
header_title.pack() #places the label on window.

current_date = time.strftime('%d-%b-%Y')    #fetches current date.

#Making Header Label
#make a label displaying 'Today' and place it at reqd location.
today_label = Label(win,text='Today:-',font=('Ariel',20,'bold'),bg='#F7CAC9',fg='black')
today_label.place(relx=0.39, rely=0.156, anchor="center")

#make a label showing current_date at reqd location.
current_date_label = Label(win,text=current_date,font=('Engravers MT',20,'bold','underline'),bg='#F7CAC9',fg='black')
current_date_label.place(relx=0.52,rely=0.154,anchor='center')

#Making Footer Label
footer_title = Label(win,text='By:Ronit Baweja\n Email:bawejaronit164@gmail.com\nProject Guide:Mr Aditya Kumar'\
                    ,font=('Eras ITC',20,'bold'),bg='#F7CAC9',fg='black')
footer_title.pack(side='bottom')

#Fetching the logo from One Drive.
img = Image.open("C:/Users/bawej/OneDrive/Desktop/coding practice/DUCAT Project 1/bank_logo.jpg").resize((240,150))
bitmap_img = ImageTk.PhotoImage(img,master=win) #converts .jpg image into a format for Tkinter library.

#Placing the logo in top-left corner.
logo_label1 = Label(win,image=bitmap_img)  #Create a widget to display image on parent window win, uses the bitmap_img object.
logo_label1.place(relx=0,rely=0) #places image at top-left corner.

logo_label2 = Label(win,image=bitmap_img)
logo_label2.place(relx=1,rely=0,anchor='ne') #places image at top-right corner.

def main_screen():
    #creates a frame on parent window,border color->black and border thichness->2pixels.
    frm = Frame(win,highlightbackground='black',highlightthickness=2)   
    frm.configure(background='#D3D3D3') #sets frame color to gray.
    frm.place(relx=0,rely=0.223,relwidth=1,relheight=0.63)  #places frame on parent window.

    #Reset Button Logic.
    def reset():
        acn_entry.delete(0,'end')   #Clear account entry.
        pass_entry.delete(0,'end')  #Clear password entry.
        return

    #Creating a login_click function.
    def login_click():
        global uacn
        uacn = acn_entry.get()
        upass = pass_entry.get()
        urole = role_cb.get()

        #Check if all details are entered or not.
        if len(uacn) == 0 or len(upass) == 0:
            messagebox.showerror('Login','Please enter all required details😩')
            return

        #Check if the account number entered is digits only.
        if not uacn.isdigit():
            messagebox.showerror('Login','Invalid Account Number, enter digits only')
            acn_entry.delete(0,'end')
            return
        
        uacn = int(uacn)    #Convert valid acn to int for further code.

        if (uacn == 0 and urole == 'Admin' and upass == 'admin'):
            frm.destroy()
            welcome_admin_screen()
        elif urole == 'User':
            #Here we will verify from our database whether the credentials entered
            #by user are valid or not. 

            #Creating a connection object with SQLite database.
            con_obj = sqlite3.connect(database='bank.sqlite')   #connection object.
            cur_obj = con_obj.cursor()  #cursor object.

            #Query to fetch credentials of user with given acno and pass if exists else None.
            cur_obj.execute('select * from users where users_acno=? and users_pass=?',(uacn,upass))
            tup = cur_obj.fetchone()  #Fetch the first record from cur_obj. If no record found then None.

            if tup == None: #If no record found then show error
                messagebox.showerror('Login','Invalid ACN/Password')
            else:
                global uname    
                uname = tup[2]  #extract username from tuple.
                frm.destroy()
                welcome_user_screen()
        else:
            messagebox.showerror('Login','Invalid ACN/Password')


    #Creating buttons and entry boxes.

    #Creating Label for account number.
    acn_label = Label(frm,text='ACN',font=('arial',20,'bold'),bg='#D3D3D3')
    acn_label.place(relx=0.3,rely=0.1)

    #Creating Entry for account number.
    acn_entry = Entry(frm,font=('arial',20,'bold'),bd=5) #creates entry with border thickness 5 pixels.
    acn_entry.place(relx=0.45,rely=0.08)
    acn_entry.focus() #Ensures shifts focus to ACN entry field when screen loads so user can start typing.

    #Creating Label for Password.
    pass_label = Label(frm,text='Password',font=('arial',20,'bold'),bg='#D3D3D3')
    pass_label.place(relx=0.3,rely=0.2)

    #Creating Entry for password.
    pass_entry = Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    pass_entry.place(relx=0.45,rely=0.20)

    #Creating Label for Role.
    role_label = Label(frm,text='Role',bg='#D3D3D3',font=('arial',20,'bold'))
    role_label.place(relx=0.3,rely=0.3)

    #Creating Combobox for Role.
    role_cb = Combobox(frm,font=('arial',20,'bold'),values=['User','Admin'],state='readonly')
    role_cb.current(0)
    role_cb.place(relx=0.45,rely=0.31)

    #Creating a login button.
    login_btn = Button(frm,text="Login",font=('Bookman Old Style',20,'bold'),bg='powder blue',command=login_click,bd=5,fg='black')
    login_btn.place(relx=0.40,rely=0.45)

    #Creating a reset button.
    reset_btn = Button(frm,command=reset,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
    reset_btn.place(relx=0.52,rely=0.45)

    #Creating a forgot password button.
    forgot_btn = Button(frm,text='Forgot Password',font=('Bookman Old Style',20,'bold'),bg='powder blue',bd=5,fg='black',command=forgot_password_screen)
    forgot_btn.place(relx=0.40,rely=0.62)

    return


def welcome_admin_screen():
    #creates a frame on parent window,border color->black and border thichness->2pixels.
    frm = Frame(win,highlightbackground='black',highlightthickness=2)   
    frm.configure(background='#D3D3D3') #sets frame color to gray.
    frm.place(relx=0,rely=0.223,relwidth=1,relheight=0.63)  #places frame on parent window win.

    def logout_click(): #When admin wants to log out.
        response = messagebox.askyesno('Logout','Do you want to logout, Kindly Confirm')
        if response:
            frm.destroy()   #destroy the current welcome_admin_screen frame.
            main_screen()   #back to main screen.

    def create_click():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.20,rely=0.1,relwidth=0.7,relheight=0.74) #places frame on parent window frm.

        def reset():
            #Clear all the entries.
            email_entry.delete(0,'end')
            name_entry.delete(0,'end')
            mob_entry.delete(0,'end')
            adhar_entry.delete(0,'end')
            return

        def open_acn():
            uname = name_entry.get()    #fetch user name from name entry.
            uemail = email_entry.get()  #fetch user email from email entry.
            uadhar = adhar_entry.get()  #fetch adhar no from adhar entry.
            umob = mob_entry.get()      #fetch user mob from mob entry.
            ubal = 0                    #set initial balance to 0.
            upass = str(random.randint(1000000,9999999)) #generate random password for first time.

            #Checking if all details are filled or not.
            if len(uadhar) == 0 or len(umob) == 0 or len(uemail) == 0:
                messagebox.showerror('Get Password','Please enter all required details😩')
                return

            #Checking if the credentials entered are valid or not.

            #Checking if name is valid or not.
            valid_name = re.match(r"^[a-zA-Z\s]+$", uname)

            if not len(uname) == 0 and not valid_name:
                messagebox.showerror('Open Account','Invalid name, use only alphabets and spaces😩')
                name_entry.delete(0,'end')
                name_entry.focus()
                return

            #Checking if email is valid or not.
            valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', uemail)

            if not len(uemail) == 0 and not valid_email:
                messagebox.showerror('Open Account','Invalid email address😩')
                email_entry.delete(0,'end')
                email_entry.focus()
                return
            
            #Checking if mob no is valid or not.
            if len(umob) != 10 or not umob.isdigit():
                if not umob.isdigit(): #Now check for non digits. This will only be executed if length is 10 but it has non digit characters.
                    messagebox.showerror('Open Account', 'Invalid Mobile Number, enter digits only😩')
                elif len(umob) != 10:  # Check for incorrect length first
                    messagebox.showerror('Open Account', 'Invalid Mobile Number, Mobile number must be 10 digits long😩')
                mob_entry.delete(0, 'end')  # Clear the entry field regardless of the error type
                mob_entry.focus()
                return
            elif not re.fullmatch('[6-9][0-9]{9}',umob):  # Check for incorrect mobile number.
                    messagebox.showerror('Open Account', 'Invalid Mobile Number, first digit 6-9😩')
                    mob_entry.delete(0, 'end')  # Clear the entry field regardless of the error type
                    mob_entry.focus()
                    return
            
        
            valid_adhar = re.match(r'^\d{4}-\d{4}-\d{4}$', uadhar)

            #Checking if adhar no is valid or not.
            if not len(uadhar) == 0 and not valid_adhar:
                messagebox.showerror('Open Account','Invalid Adhar Number😩')
                adhar_entry.delete(0,'end')
                adhar_entry.focus()
                return

            key = 0
            
            try:
                #Make a connection to run a DQL Command.
                con_obj = sqlite3.connect(database='bank.sqlite')
                cur_obj = con_obj.cursor()

                cur_obj.execute('''select * from users where users_email = ? 
                                or users_pass = ? 
                                or users_mob = ?''',(uemail,upass,umob))
                
                userexists = cur_obj.fetchone()

                #Checking if we actually have a record in the table having entered email or adhar or mobile no.
                if userexists:
                    messagebox.showerror('Error', 'This email, mobile number, or Adhar number already exists. Please use unique values.')
                    return


                #Make a connection with database to rum DML command.
                con_obj = sqlite3.connect(database='bank.sqlite')   #connection object.
                cur_obj = con_obj.cursor()  #cursor object to run queries.

                
                #Inserting user values into users table.
                cur_obj.execute('''insert into users(users_pass ,
                                users_name,users_mob,users_email,users_bal,
                                users_adhar,users_opendate)
                                values(?,?,?,?,?,?,?)''',(upass,uname,umob,uemail,ubal,uadhar,current_date))
                con_obj.commit()
                con_obj.close()

                #Make a connection to run a DQL command 
                #as we cannot run different kind of queries on same connection.
                con_obj = sqlite3.connect(database='bank.sqlite')
                cur_obj = con_obj.cursor()

                #Query to fetch the account number of latest user created.
                cur_obj.execute('select max(users_acno) from users')    #select the latest account number as in autoincrement we have maxVal+1.
                con_obj.commit()
                tup = cur_obj.fetchone()    #fetch the record in tuple from cursor object.
                uacn = tup[0]

                con_obj.close()
            except:
                messagebox.showerror('Error', 'This email, mobile number, or Adhar number already exists. Please use unique values.')

            
            try:
                #Creating a gmail connection so that we can mail our user.
                gmail_con = gmail.GMail('bawejaronit164@gmail.com','vccs tdjh blrs inni')
                umsg = f'''Hello,{uname}
                        Welcome to ABC Bank
                        Your Account Number is:-{uacn} 
                        Your Password is:-{upass}
                        
                        Kindly change your password when you login first time🙏
                

                        Thanks'''
                
                msg = gmail.Message(to=uemail,subject='Account Opened',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('open account','account created and kindly check your email for acn/pass🤩')
                reset()

            except:
                messagebox.showerror('open ACN','Something went wrong🥺')
                

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is Create User Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        #create a name label.
        name_label = Label(ifrm,text='Name',font=('arial',20,'bold'),bg='white',fg='black')
        name_label.place(relx=0.2,rely=0.2)

        #create a name entry.
        name_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        name_entry.configure(bg='#EED9C4')
        name_entry.place(relx=0.5,rely=0.2)
        name_entry.focus()

        #create a email label.
        email_label = Label(ifrm,text='Email',font=('arial',20,'bold'),bg='white',fg='black')
        email_label.place(relx=0.2,rely=0.35)

        #create a email entry.
        email_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        email_entry.configure(bg='#EED9C4')
        email_entry.place(relx=0.5,rely=0.35)

        #create a adhar label.
        adhar_label = Label(ifrm,text='Adhar',font=('arial',20,'bold'),bg='white',fg='black')
        adhar_label.place(relx=0.2,rely=0.5)

        #create a adhar entry.
        adhar_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        adhar_entry.configure(bg='#EED9C4')
        adhar_entry.place(relx=0.5,rely=0.5)

        #create a mob label.
        mob_label = Label(ifrm,text='Mobile Number',font=('arial',20,'bold'),bg='white',fg='black')
        mob_label.place(relx=0.2,rely=0.65)

        #create a mob entry.
        mob_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        mob_entry.configure(bg='#EED9C4')
        mob_entry.place(relx=0.5,rely=0.65)

        #Create an open button
        open_button = Button(ifrm,command=open_acn,text='Open',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        open_button.place(relx=0.5,rely=0.8)

        #Create a reset button
        reset_button = Button(ifrm,command=reset,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        reset_button.place(relx=0.65,rely=0.8)

    def view_click():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.20,rely=0.1,relwidth=0.7,relheight=0.74) #places frame on parent window frm.

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is View User Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        #create a acn label.
        acn_label = Label(ifrm,text='ACN',font=('arial',20,'bold'),bg='white',fg='black')
        acn_label.place(relx=0.3,rely=0.3)

        #create a acn entry.
        acn_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        acn_entry.configure(bg='#EED9C4')
        acn_entry.place(relx=0.5,rely=0.3)
        acn_entry.focus()

        def view_user(ifrm):
            """Displays user data in a formatted Treeview with bold headings and lines."""
            try:
                con = sqlite3.connect('bank.sqlite')
                cursor = con.cursor()

                cursor.execute("SELECT * FROM users")
                data = cursor.fetchall()
                con.close()

                column_names = [description[0] for description in cursor.description]

                tree = ttk.Treeview(ifrm, columns=column_names, show="headings")

                # Configure style for bold headings and lines
                style = ttk.Style()
                style.configure("Treeview.Heading", font=('TkDefaultFont', 10, 'bold'))  # Bold headings
                style.configure("Treeview", rowheight=25) # Adjust row height for better visibility

                # Set column headings with formatting
                for col in column_names:
                    tree.heading(col, text=col, anchor="center")  # Center headings
                    tree.column(col, width=150, anchor='w', stretch=False)  # Adjust width and prevent stretching
                    
                # Insert data with alternating row colors for better readability
                for i, row in enumerate(data):
                    tree.insert("", "end", values=row, tags=("row",))
                    tree.tag_configure("row", background= "#f0f0f0" if i % 2 == 0 else "white") # Alternating row colors


                # Add separator lines between columns (using canvas)
                def add_separators(event=None):
                    x = 0  # Start at the left edge of the Treeview
                    for col in column_names[:-1]:  # Exclude the last column
                        x += tree.column(col, 'width')
                        tree.canvas.create_line(x, 0, x, tree.winfo_height(), width=1, tags="separator")

                # Add scrollbars
                vsb = ttk.Scrollbar(ifrm, orient="vertical", command=tree.yview)
                vsb.pack(side='right', fill='y')
                tree.configure(yscrollcommand=vsb.set)

                hsb = ttk.Scrollbar(ifrm, orient="horizontal", command=tree.xview)
                hsb.pack(side='bottom', fill='x')
                tree.configure(xscrollcommand=hsb.set)

                tree.pack(fill="both", expand=True)

            except sqlite3.Error as e:
                messagebox.showerror('Error', 'Database Error')
                print(f"Database Error: {e}")

        view_user(ifrm)

        '''
        #Create an view button
        view_button = Button(ifrm,text='View',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        view_button.place(relx=0.5,rely=0.7)

        #Create a reset button
        reset_button = Button(ifrm,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        reset_button.place(relx=0.63,rely=0.7)'''

    def delete_click():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.20,rely=0.1,relwidth=0.7,relheight=0.74) #places frame on parent window frm.

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is Delete User Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        #Reset button logic.
        def reset():
            data = acn_entry.get()
            acn_entry.delete(0,len(data))  #clear the entry field.

        def delete_user():
            acno = acn_entry.get()

            #Checking if account number is digits only.
            if not acno.isdigit():
                messagebox.showerror('Delete User','Invalid Account Number, enter digits only.')
                reset()
                return
            
            acno = int(acno)  #Convert acn to int for future code.  

            #Fetching details of user to check if the acn is valid or not.
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute('select * from users where users_acno = ?',(acno,))
            con_obj.commit()
            tup = cur_obj.fetchone()

            if tup == None: #No such user exists.
                messagebox.showerror('Delete User','User does not exist🙄')
                reset()  #clear the entry field.
                return
            
            var = messagebox.askyesnocancel('Delete User','Do you really want to delete?')

            if not var:
                reset()
                return
            
            #Deleting the user from our database.
            con_obj = sqlite3.connect(database='bank.sqlite')   #connection object
            cur_obj = con_obj.cursor()  #cursor object
            cur_obj.execute('delete from users where users_acno = ?',(acno,))
            cur_obj.execute('delete from txn where txn_acno = ?',(acno,))
            con_obj.commit()
            con_obj.close()
            acn_entry.delete(0,'end')   #clear acn entry.

            #Updating the sqlite_sequence table to maintain the sequence of auto increment.
            con_obj = sqlite3.connect('bank.sqlite')
            cur_obj = con_obj.cursor()

            cur_obj.execute('''update sqlite_sequence set seq 
                            = (select MAX(users_acno) from users) 
                            where name = ?''',('users',))
            con_obj.commit()
            con_obj.close()
            print('Update successful!!')

            messagebox.showinfo('Delete',f'User with ACN {acno} deleted successfully💫')
            return

        #create a acn label.
        acn_label = Label(ifrm,text='ACN',font=('arial',20,'bold'),bg='white',fg='black')
        acn_label.place(relx=0.3,rely=0.3)

        #create a acn entry.
        acn_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        acn_entry.configure(bg='#EED9C4')
        acn_entry.place(relx=0.5,rely=0.3)
        acn_entry.focus()

        #Create an delete button
        delete_button = Button(ifrm,command=delete_user,text='Delete',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        delete_button.place(relx=0.5,rely=0.7)

        #Create a reset button
        reset_button = Button(ifrm,command=reset,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        reset_button.place(relx=0.65,rely=0.7)

    def update_click1():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.20,rely=0.1,relwidth=0.7,relheight=0.74) #places frame on parent window frm.

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is Update User Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        #Reset back button logic.
        def back_click():
            ifrm2.place_forget()  # Hide ifrm2
            ifrm.place(relx=0.20, rely=0.1, relwidth=0.7, relheight=0.74)  # Show ifrm1
            # Restore any other widgets that were hidden
        
        def reset():
            acn_entry.delete(0,'end')
            return
        

        def update_details():
            uacn = acn_entry.get()  #Fetch email from entry.

            #Check if empty field or not.
            if len(uacn) == 0:
                messagebox.showerror('Update Details','Please enter all required details😩')
                return
            
            #Check if acn is valid or not.
            if not len(uacn) == 0 and not uacn.isdigit():
                messagebox.showerror('Update Details','Invalid Account Number, enter digits only😩')
                acn_entry.delete(0,'end')
                acn_entry.focus()
                return
            
            uacn = int(uacn)

            #Now checking if this account exists or not.
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()

            cur_obj.execute('select * from users where users_acno = ?',(uacn,))
            con_obj.commit()
            tup = cur_obj.fetchone()
            con_obj.close()

            #Check if tup is None or not.
            if tup == None:
                messagebox.showerror('Update User','User does not exist💀')
                acn_entry.delete(0,'end')
                return
            
            global ifrm2
            ifrm2 = Frame(frm, highlightbackground='black', highlightthickness=3)  # Give it a name
            ifrm2.configure(bg='white')
            ifrm2.place(relx=0.20, rely=0.1, relwidth=0.7, relheight=0.74)  # Place it initially, but it will be hidden

            heading_ifrm2 = Label(ifrm2, text='This is Update User Screen', font=('Brush Script MT', 30, 'bold'), bg='white', fg='purple')
            heading_ifrm2.pack()

            #create a name label.
            name_label = Label(ifrm2,text='Name',font=('arial',20,'bold'),bg='white',fg='black')
            name_label.place(relx=0.2,rely=0.2)

            #create a name entry.
            name_entry = Entry(ifrm2,font=('arial',20,'bold'),bd=5)
            name_entry.configure(bg='#EED9C4')
            name_entry.place(relx=0.5,rely=0.2)
            name_entry.insert(0,tup[2]) #Insert current user name into the name entry.
            name_entry.focus()

            #create a email label.
            email_label = Label(ifrm2,text='Email',font=('arial',20,'bold'),bg='white',fg='black')
            email_label.place(relx=0.2,rely=0.35)

            #create a email entry.
            email_entry = Entry(ifrm2,font=('arial',20,'bold'),bd=5)
            email_entry.configure(bg='#EED9C4')
            email_entry.place(relx=0.5,rely=0.35)
            email_entry.insert(0,tup[4]) #Insert current user email into email entry.

            #create a mob label.
            mob_label = Label(ifrm2,text='Mobile Number',font=('arial',20,'bold'),bg='white',fg='black')
            mob_label.place(relx=0.2,rely=0.65)

            #create a mob entry.
            mob_entry = Entry(ifrm2,font=('arial',20,'bold'),bd=5)
            mob_entry.configure(bg='#EED9C4')
            mob_entry.place(relx=0.5,rely=0.65)
            mob_entry.insert(0,tup[3])  #Insert current mob no into mob entry.

            #create a password label.
            pass_label = Label(ifrm2,text='Password',font=('arial',20,'bold'),bg='white',fg='black')
            pass_label.place(relx=0.2,rely=0.5)

            #create a pass entry.
            pass_entry = Entry(ifrm2,font=('arial',20,'bold'),bd=5)
            pass_entry.configure(bg='#EED9C4')
            pass_entry.place(relx=0.5,rely=0.5)
            pass_entry.insert(0,tup[1]) #Insert current password into pass_entry.

            def reset1():
                pass_entry.delete(0,'end')
                mob_entry.delete(0,'end')
                name_entry.delete(0,'end')
                email_entry.delete(0,'end')

            def update_details2():
                uname = name_entry.get()    #Fetching updated values of all records.
                upass = pass_entry.get()
                umob = mob_entry.get()
                uemail = email_entry.get()

                #Checking if all details are filled or not.
                if len(uname) == 0 or len(umob) == 0 or len(uemail) == 0 or len(upass) == 0:
                    messagebox.showerror('Update Details','Please enter all required details😩')
                    return

                #Checking if name is valid or not.
                valid_name = re.match(r"^[a-zA-Z\s]+$", uname)

                if not len(uname) == 0 and not valid_name:
                    messagebox.showerror('Open Account','Invalid name, use only alphabets and spaces😩')
                    name_entry.delete(0,'end')
                    name_entry.focus()
                    return

                #Checking if email is valid or not.
                valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', uemail)

                if not len(uemail) == 0 and not valid:
                    messagebox.showerror('Update Details','Invalid email address😩')
                    email_entry.delete(0,'end')
                    return
                
                #Checking if mob no is valid or not.
                if len(umob) != 10 or not umob.isdigit():
                    if not umob.isdigit(): #Now check for non digits. This will only be executed if length is 10 but it has non digit characters.
                        messagebox.showerror('Update Details', 'Invalid Mobile Number, enter digits only😩')
                    elif len(umob) != 10:  # Check for incorrect length first
                        messagebox.showerror('Update Details', 'Invalid Mobile Number, Mobile number must be 10 digits long😩')
                    mob_entry.delete(0, 'end')  # Clear the entry field regardless of the error type
                    mob_entry.focus()
                    return
                elif not re.fullmatch('[6-9][0-9]{9}',umob):  # Check for incorrect mobile number.
                        messagebox.showerror('Update Details', 'Invalid Mobile Number, first digit 6-9😩')
                        mob_entry.delete(0, 'end')  # Clear the entry field regardless of the error type
                        mob_entry.focus()
                        return

                #Need to check whether the new mobile number or email are taken in some other entry or not.
                con_obj = sqlite3.connect(database='bank.sqlite')
                cur_obj = con_obj.cursor()

                cur_obj.execute('''select * from users where 
                                (users_email = ? or users_pass = ?)
                                and users_acno != ?''',(uemail,upass,uacn))
                con_obj.commit()
                
                #Checking if a user already has such credentials or not.
                existing_user = cur_obj.fetchone()

                if existing_user:
                    messagebox.showerror('Error', 'This email or mobile number already exists. Please use unique values.')
                    return
                
                con_obj.close()

                #Now since we know that our data is safe to be updated so we run the update query.
                
                con_obj = sqlite3.connect(database='bank.sqlite')   #connection object to run DML command.
                cur_obj = con_obj.cursor()  #cursor object to run queries.
                #Running an update query.
                cur_obj.execute('update users set users_name=?,users_pass=?,users_mob=?,users_email=? where users_acno=?',(uname,upass,umob,uemail,uacn))
                con_obj.commit()    #Confirm DML command status.
                messagebox.showinfo('Update','Update Successful🎉')
                ifrm2.destroy()  #Backtrack 1 step.


            #Create a back button.
            back_button = Button(ifrm2,command=back_click,text='Back',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
            back_button.place(relx=0,rely=0)

            #Create an update button.
            update_button = Button(ifrm2,command=update_details2,text='Update',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
            update_button.place(relx=0.5,rely=0.8)

            #Create a reset button.
            reset_button = Button(ifrm2,command=reset1,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
            reset_button.place(relx=0.665,rely=0.8)

            ifrm.place_forget() # Hide ifrm
            ifrm2.place(relx=0.20, rely=0.1, relwidth=0.7, relheight=0.74) #Show ifrm2.


        #create a acn label.
        acn_label = Label(ifrm,text='ACN',font=('arial',20,'bold'),bg='white',fg='black')
        acn_label.place(relx=0.3,rely=0.3)

        #create a acn entry.
        acn_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        acn_entry.configure(bg='#EED9C4')
        acn_entry.place(relx=0.5,rely=0.3)
        acn_entry.focus()

        #Create an update button.
        update_button = Button(ifrm,command=update_details,text='Update',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        update_button.place(relx=0.5,rely=0.7)

        #Create a reset button.
        reset_button = Button(ifrm,command=reset,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        reset_button.place(relx=0.665,rely=0.7)

    wel_label=Label(frm,font=('arial',20,'bold'),text="Welcome Admin",fg='#B10000')
    wel_label.place(relx=0,rely=0)

    #Creating a logout button.
    logout_btn = Button(frm,text='Logout',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=logout_click)
    logout_btn.place(relx=0.90,rely=0.85)

    #Creating a create button.
    create_btn = Button(frm,width=12,text='Create User',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=create_click)
    create_btn.place(relx=0,rely=0.1)

    #Creating a view button.
    view_btn = Button(frm,width=12,text='View Users',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=view_click)
    view_btn.place(relx=0,rely=0.3)

    #Creating a delete button.
    delete_btn = Button(frm,width=12,text='Delete User',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=delete_click)
    delete_btn.place(relx=0,rely=0.5)

    #Creating a update button
    update_btn = Button(frm,width=12,text='Update User',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=update_click1)
    update_btn.place(relx=0,rely=0.7)



def forgot_password_screen():
    #creates a frame on parent window,border color->black and border thichness->2pixels.
    frm = Frame(win,highlightbackground='black',highlightthickness=2)   
    frm.configure(background='#D3D3D3') #sets frame color to gray.
    frm.place(relx=0,rely=0.223,relwidth=1,relheight=0.63)  #places frame on parent window.

    def back_click():
        frm.destroy()
        main_screen()

    def reset():
        acn_entry.delete(0,'end')   #Clear all entries.
        mob_entry.delete(0,'end')
        email_entry.delete(0,'end')

    def get_password():
        uacn = acn_entry.get()      #Fetch all the values from respective entries.
        uemail = email_entry.get()
        umob = mob_entry.get()

        #Checking if all details are filled or not.
        if len(uacn) == 0 or len(umob) == 0 or len(uemail) == 0:
            messagebox.showerror('Get Password','Please enter all required details😩')
            return

        #Check if acn is valid or not.
        if not len(uacn) == 0 and not uacn.isdigit():
            messagebox.showerror('Get Password','Invalid Account Number, enter digits only😩')
            acn_entry.delete(0,'end')
            acn_entry.focus()
            return

        #Checking if email is valid or not.
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', uemail)

        if not len(uemail) == 0 and not valid:
            messagebox.showerror('Get Password','Invalid email address😩')
            email_entry.delete(0,'end')
            email_entry.focus()
            return
        
        #Checking if mob no is valid or not.
        if len(umob) != 10 or not umob.isdigit():
            if not umob.isdigit(): #Now check for non digits. This will only be executed if length is 10 but it has non digit characters.
                messagebox.showerror('Get Password', 'Invalid Mobile Number, enter digits only😩')
            elif len(umob) != 10:  # Check for incorrect length first
                messagebox.showerror('Get Password', 'Invalid Mobile Number, Mobile number must be 10 digits long😩')
            mob_entry.delete(0, 'end')  # Clear the entry field regardless of the error type
            mob_entry.focus()
            return
        elif not re.fullmatch('[6-9][0-9]{9}',umob):  # Check for incorrect mobile number.
                    messagebox.showerror('Get Password', 'Invalid Mobile Number, first digit 6-9😩')
                    mob_entry.delete(0, 'end')  # Clear the entry field regardless of the error type
                    mob_entry.focus()
                    return
        
    
        con_obj = sqlite3.connect(database='bank.sqlite')   #connection object.
        cur_obj = con_obj.cursor()  #cursor object.
        cur_obj.execute('select * from users where users_acno=? and users_email=? and users_mob=?',(uacn,uemail,umob))
        tup = cur_obj.fetchone()    #fetch details in a tuple.

        if tup == None:
            messagebox.showerror('forgot password','Invalid Details💀')
        else:
            try:
                gmail_con = gmail.GMail('bawejaronit164@gmail.com','vccs tdjh blrs inni')
                umsg = f'''Hello {tup[2]}
                        Welcome to ABC Bank
                        
                        Your ACN is {tup[0]}
                        Your Password is {tup[1]}

                        Thanks'''
                
                msg = gmail.Message(to=uemail,subject='Password Recovery',text=umsg)
                gmail_con.send(msg)
                print('Password Recoverd')
                messagebox.showinfo('forgot password','kindly check your email for password')
                back_click()
            except:
                messagebox.showerror('Forgot Password','Something went wrong🥺')
            

    #Creating a back button.
    back_btn = Button(frm,command=back_click,width=12,text='Back',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
    back_btn.place(relx=0,rely=0)

    #Creating an account label.
    acn_label = Label(frm,text='ACN',font=('arial',20,'bold'),bg='#D3D3D3')
    acn_label.place(relx=0.32,rely=0.2)

    #Creating an account entry.
    acn_entry = Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.focus()
    acn_entry.place(relx=0.45,rely=0.18)

    #Creating an email label.
    email_label = Label(frm,text='Email',font=('arial',20,'bold'),bg='#D3D3D3')
    email_label.place(relx=0.32,rely=0.31)

    #Creating an email entry.
    email_entry = Entry(frm,font=('arial',20,'bold'),bd=5)
    email_entry.place(relx=0.45,rely=0.3)

    #Creating a mobile label.
    mob_label = Label(frm,text='Mobile No',font=('arial',20,'bold'),bg='#D3D3D3')
    mob_label.place(relx=0.32,rely=0.43)

    #Creating a mobile entry.
    mob_entry = Entry(frm,font=('arial',20,'bold'),bd=5)
    mob_entry.place(relx=0.45,rely=0.42)

    #Creating submit button.
    submit_btn = Button(frm,command=get_password,text='Submit',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
    submit_btn.place(relx=0.48,rely=0.58)

    #Creating reset button.
    submit_btn = Button(frm,command=reset,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
    submit_btn.place(relx=0.61,rely=0.58)

def welcome_user_screen():
    #creates a frame on parent window,border color->black and border thichness->2pixels.
    frm = Frame(win,highlightbackground='black',highlightthickness=2)   
    frm.configure(background='#D3D3D3') #sets frame color to gray.
    frm.place(relx=0,rely=0.223,relwidth=1,relheight=0.63)  #places frame on parent window win.

    def logout_click(): #When admin wants to log out
        response = messagebox.askyesno('Logout','Do you want to logout, Kindly Confirm')
        if response:
            frm.destroy()   #destroy the current welcome_admin_screen frame.
            main_screen()   #back to main screen.

    def check_click():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.65,relheight=0.74) #places frame on parent window frm.

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is Check Balance Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        #Here we need to check the account balance of user.
        con_obj = sqlite3.connect(database='bank.sqlite')   #connection object.
        cur_obj = con_obj.cursor()  #cursor object.
        cur_obj.execute('select * from users where users_acno=?',(uacn,))
        tup = cur_obj.fetchone()
        con_obj.close()

        #Now we place one label each of every detail that we want to display about user.
        name_label1 = Label(ifrm,text=f'UserName:-',fg='#E32636',bg='white',font=('Brush Script MT',25,'bold')) #Create a name label with Cardinal color.
        name_label1.place(relx=0.15,rely=0.2)

        name_label2 = Label(ifrm,text=tup[2],font=('Edwardian Script ITC',30,'bold'),fg='#D94972',bg='white')   #Fill the name value with Cabaret color.
        name_label2.place(relx=0.4,rely=0.18)

        acn_label1 = Label(ifrm,text='Account No:-',font=('Brush Script MT',25,'bold'),fg='#E32636',bg='white') #Create a acno label with Cardinal color.
        acn_label1.place(relx=0.15,rely=0.35)

        acn_label2 = Label(ifrm,text=tup[0],font=('Monotype Corsiva',30,'bold'),bg='white',fg='#D94972')    #Fill the acno value with Cabaret color.
        acn_label2.place(relx=0.4,rely=0.32)

        bal_label1 = Label(ifrm,text='Balance:-',font=('Brush Script MT',25,'bold'),bg='white',fg='#E32636')    #Create a bal label with Cardinal color.
        bal_label1.place(relx=0.15,rely=0.50)

        bal_label2 = Label(ifrm,text=tup[5],font=('Monotype Corsiva',30,'bold'),bg='white',fg='#D94972')    #Fill the bal value with Cabaret color.
        bal_label2.place(relx=0.4,rely=0.48)

        adhar_label1 = Label(ifrm,text='Adhar No:-',font=('Brush Script MT',25,'bold'),bg='white',fg='#E32636') #Create a adhar label with Cardinal color.
        adhar_label1.place(relx=0.15,rely=0.65)

        adhar_label2 = Label(ifrm,text=tup[6],font=('Monotype Corsiva',30,'bold'),bg='white',fg='#D94972')  #Fill the adhar value with Cabaret color.
        adhar_label2.place(relx=0.4,rely=0.62)

        opendate_label1 = Label(ifrm,text='Opendate:-',font=('Brush Script MT',25,'bold'),bg='white',fg='#E32636') #Create a opendate label with Cardinal color.
        opendate_label1.place(relx=0.15,rely=0.80)

        opendate_label2 = Label(ifrm,text=tup[7],font=('Monotype Corsiva',30,'bold'),bg='white',fg='#D94972') #Fill the opendate value with Cabaret color.
        opendate_label2.place(relx=0.4,rely=0.78)

    def update_click():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.65,relheight=0.74) #places frame on parent window frm.

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is Update Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        def reset():
            mob_entry.delete(0,'end')   #Clear all entries
            name_entry.delete(0,'end')
            pass_entry.delete(0,'end')
            email_entry.delete(0,'end')
            return

        def update_details():
            uname = name_entry.get()    #Fetching updated values of all records.
            upass = pass_entry.get()
            umob = mob_entry.get()
            uemail = email_entry.get()

            #Checking if all details are filled or not.
            if len(uname) == 0 or len(umob) == 0 or len(uemail) == 0 or len(upass) == 0:
                messagebox.showerror('Update Details','Please enter all required details😩')
                return

            #Checking if name is valid or not.
            valid_name = re.match(r"^[a-zA-Z\s]+$", uname)

            if not len(uname) == 0 and not valid_name:
                messagebox.showerror('Open Account','Invalid name, use only alphabets and spaces😩')
                name_entry.delete(0,'end')
                name_entry.focus()
                return

            #Checking if email is valid or not.
            valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', uemail)

            if not len(uemail) == 0 and not valid:
                messagebox.showerror('Update Details','Invalid email address😩')
                email_entry.delete(0,'end')
                return
            
            #Checking if mob no is valid or not.
            if len(umob) != 10 or not umob.isdigit():
                if not umob.isdigit(): #Now check for non digits. This will only be executed if length is 10 but it has non digit characters.
                    messagebox.showerror('Update Details', 'Invalid Mobile Number, enter digits only😩')
                elif len(umob) != 10:  # Check for incorrect length first
                    messagebox.showerror('Update Details', 'Invalid Mobile Number, Mobile number must be 10 digits long😩')
                mob_entry.delete(0, 'end')  # Clear the entry field regardless of the error type
                mob_entry.focus()
                return
            elif not re.fullmatch('[6-9][0-9]{9}',umob):  # Check for incorrect mobile number.
                    messagebox.showerror('Update Details', 'Invalid Mobile Number, first digit 6-9😩')
                    mob_entry.delete(0, 'end')  # Clear the entry field regardless of the error type
                    mob_entry.focus()
                    return
    

            #Need to check whether the new mobile number or email are taken in some other entry or not.
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()

            cur_obj.execute('''select * from users where 
                            (users_email = ? or users_pass = ?)
                            and users_acno != ?''',(uemail,upass,uacn))
            con_obj.commit()
            
            #Checking if a user already has such credentials or not.
            existing_user = cur_obj.fetchone()

            if existing_user:
                messagebox.showerror('Error', 'This email or mobile number already exists. Please use unique values.')
                return
            
            con_obj.close()


            #Now since we know that our data is safe to be updated so we run the update query.     
            con_obj = sqlite3.connect(database='bank.sqlite')   #connection object to run DML command.
            cur_obj = con_obj.cursor()  #cursor object to run queries.
            #Running an update query.
            cur_obj.execute('update users set users_name=?,users_pass=?,users_mob=?,users_email=? where users_acno=?',(uname,upass,umob,uemail,uacn))
            con_obj.commit()    #Confirm DML command status.
            messagebox.showinfo('Update','Update Successful🎉')
            con_obj.close()

            ifrm.destroy()  #Backtrack 1 step.

        con_obj = sqlite3.connect(database='bank.sqlite')   #create a connection object to database.
        cur_obj = con_obj.cursor()  #create a cursor object.

        #fetching all the details of user whose credentials need to be updated.
        cur_obj.execute('select * from users where users_acno = ?',(uacn,))

        tup = cur_obj.fetchone()    #fetch data from tuple.
        con_obj.close()

        #create a name label.
        name_label = Label(ifrm,text='Name',font=('arial',20,'bold'),bg='white',fg='black')
        name_label.place(relx=0.2,rely=0.2)

        #create a name entry.
        name_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        name_entry.configure(bg='#EED9C4')
        name_entry.place(relx=0.5,rely=0.2)
        name_entry.insert(0,tup[2]) #Insert current user name into the name entry.
        name_entry.focus()

        #create a email label.
        email_label = Label(ifrm,text='Email',font=('arial',20,'bold'),bg='white',fg='black')
        email_label.place(relx=0.2,rely=0.35)

        #create a email entry.
        email_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        email_entry.configure(bg='#EED9C4')
        email_entry.place(relx=0.5,rely=0.35)
        email_entry.insert(0,tup[4]) #Insert current user email into email entry.

        #create a mob label.
        mob_label = Label(ifrm,text='Mobile Number',font=('arial',20,'bold'),bg='white',fg='black')
        mob_label.place(relx=0.2,rely=0.65)

        #create a mob entry.
        mob_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        mob_entry.configure(bg='#EED9C4')
        mob_entry.place(relx=0.5,rely=0.65)
        mob_entry.insert(0,tup[3])  #Insert current mob no into mob entry.

        #create a password label.
        pass_label = Label(ifrm,text='Password',font=('arial',20,'bold'),bg='white',fg='black')
        pass_label.place(relx=0.2,rely=0.5)

        #create a pass entry.
        pass_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        pass_entry.configure(bg='#EED9C4')
        pass_entry.place(relx=0.5,rely=0.5)
        pass_entry.insert(0,tup[1]) #Insert current password into pass_entry.

        #Create an update button
        update_button = Button(ifrm,command=update_details,text='Update',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        update_button.place(relx=0.5,rely=0.8)

        #Create a reset button
        reset_button = Button(ifrm,command=reset,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        reset_button.place(relx=0.7,rely=0.8)

    
    def deposit_click():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.65,relheight=0.74) #places frame on parent window frm.

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is Deposit Amount Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        def reset():
            amt_entry.delete(0,'end')
            amt_entry.focus()
            return

        def deposit_amt():
            uamt = amt_entry.get()   #Amount to be withdrawn

            #Checking if amount entered is valid or not.
            if not uamt.isdigit():
                messagebox.showerror('Withdraw','Invalid Amount Entered😩')
                reset()
                return

            uamt = float(uamt)  #Convert amt to float for future code.

            con_obj = sqlite3.connect(database='bank.sqlite')   #connection object.
            cur_obj = con_obj.cursor()  #cursor object.
            cur_obj.execute('select * from users where users_acno = ?',(uacn,)) #fetch details of current user.
            con_obj.commit()

            tup = cur_obj.fetchone() #Fetch details of user in tuple.
            ubal = tup[5]  #current balance of user.
            con_obj.close()


            #We need to make the connection again as we run a DML command this time.
            con_obj = sqlite3.connect(database='bank.sqlite')   #connection object.
            cur_obj = con_obj.cursor()  #cursor object.

            #Query to update the balance after deposit.
            cur_obj.execute('update users set users_bal = ? where users_acno = ?',(ubal+uamt,uacn))
            con_obj.commit()    #commit execution of query.
            con_obj.close()

            #Now we need to update this deposit in transaction table as well.

            con_obj = sqlite3.connect(database='bank.sqlite')    #connection object.
            cur_obj = con_obj.cursor()  #cursor object.

            cur_obj.execute('''insert into txn
                            (txn_acno,txn_type,txn_date,txn_amt,txn_updatebal)
                             values(?,?,?,?,?)'''\
                            ,(uacn,'Cr(+)',time.strftime('%d-%b-%Y %r'),uamt,ubal+uamt))
            con_obj.commit()
            con_obj.close()

            messagebox.showinfo('Deposit',f'Deposited {uamt}, updated balance is {uamt+ubal}')
            amt_entry.delete(0,'end')


        #create a acn label.
        amt_label = Label(ifrm,text='Enter Amount',font=('arial',20,'bold'),bg='white',fg='black')
        amt_label.place(relx=0.2,rely=0.3)

        #create an amount entry.
        amt_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        amt_entry.configure(bg='#EED9C4')
        amt_entry.place(relx=0.5,rely=0.3)
        amt_entry.focus()

        #Create a deposit button
        deposit_button = Button(ifrm,command=deposit_amt,text='Deposit',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        deposit_button.place(relx=0.5,rely=0.7)

        #Create a reset button
        reset_button = Button(ifrm,command=reset,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        reset_button.place(relx=0.7,rely=0.7)


    def withdraw_click():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.65,relheight=0.74) #places frame on parent window frm.

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is Withdraw Amount Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        def reset():
            amt_entry.delete(0,'end')
            amt_entry.focus()
            return

        def withdraw_amt():
            uamt = amt_entry.get()   #Amount to be withdrawn

            #Checking if amount entered is valid or not.
            if not uamt.isdigit():
                messagebox.showerror('Withdraw','Invalid Amount Entered😩')
                reset()
                return

            uamt = float(uamt)  #Convert amt to float for future code.

            #Fetch the current account balance.
            con_obj = sqlite3.connect(database='bank.sqlite')   #connection object.
            cur_obj = con_obj.cursor()  #cursor object.
            cur_obj.execute('select users_bal from users where users_acno = ?',(uacn,))
            con_obj.commit()

            #Fetch the user data in a tuple.
            tup = cur_obj.fetchone()
            ubal = tup[0]   #Current balance of user.
            con_obj.close()

            #Check if sufficient balance is there to withdraw.
            if (ubal >= uamt):
                updated_bal = ubal - uamt
                
                #Update the user balance in the main database.
                con_obj = sqlite3.connect(database='bank.sqlite')
                cur_obj = con_obj.cursor()

                cur_obj.execute('update users set users_bal = ? where users_acno = ?',(updated_bal,uacn,))
                con_obj.commit()
                con_obj.close()

                #Update the transaction table.
                con_obj = sqlite3.connect(database='bank.sqlite')
                cur_obj = con_obj.cursor()

                cur_obj.execute('''insert into txn
                                (txn_acno,txn_type,txn_date,txn_amt,txn_updatebal)
                                values(?,?,?,?,?)''',(uacn,'Db(-)',time.strftime('%d-%b-%d %H:%M:%S %p'),uamt,updated_bal))
                
                con_obj.commit()
                con_obj.close()

                messagebox.showinfo('Withdraw',f'Withdrawn {uamt}, updated balance is {updated_bal}😏')
                amt_entry.delete(0,'end')

            #When balance is not sufficient to withdraw.
            else:
                messagebox.showerror('withdraw','Insufficient Balance👀')

        #create a acn label.
        amt_label = Label(ifrm,text='Enter Amount',font=('arial',20,'bold'),bg='white',fg='black')
        amt_label.place(relx=0.2,rely=0.3)

        #create an amount entry.
        amt_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        amt_entry.configure(bg='#EED9C4')
        amt_entry.place(relx=0.5,rely=0.3)
        amt_entry.focus()

        #Create a withdraw button
        withdraw_button = Button(ifrm,command=withdraw_amt,text='Withdraw',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        withdraw_button.place(relx=0.5,rely=0.7)

        #Create a reset button
        reset_button = Button(ifrm,command=reset,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        reset_button.place(relx=0.725,rely=0.7)

    def transfer_click():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.65,relheight=0.74) #places frame on parent window frm.

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is Transfer Amount Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        def reset():
            amt_entry.delete(0,'end')
            to_entry.delete(0,'end')
            to_entry.focus()
            return

        def transfer_amt():
            uamt = amt_entry.get()  #Fetch amount from entry.
            to_acn = to_entry.get() #Fetch to_acn from entry.

            #Checking if amount entered is valid or not.
            if not len(uamt) == 0 and not uamt.isdigit():
                messagebox.showerror('Transfer Amount','Invalid Amount, enter digits only😩')
                amt_entry.delete(0,'end')
                return

            #Checking if to_acn is valid or not.
            if not len(to_acn) == 0 and not to_acn.isdigit():
                messagebox.showerror('Transfer Amount','Invalid Account Number, enter digits only😩')
                to_entry.delete(0,'end')
                return

            #Checking if all details are filled or not.
            if len(to_acn) == 0 or len(uamt) == 0 :
                messagebox.showerror('Transfer Amount','Please enter all required details😩')
                return
            
            uamt = float(uamt)  #Converting amount to float for further code use.
            to_acn = int(to_acn)    #Converting to_acn to int for further code use.

            #Checking if to_acn and uacn are same.
            if to_acn == uacn:
                messagebox.showerror('Transfer Amount','Cannot transfer money to same account😒')
                to_entry.delete(0,'end')
                return

            #Now we need to check the current balance of user who is sending money.
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()

            cur_obj.execute('select * from users where users_acno = ?',(uacn,))
            con_obj.commit()
            tup = cur_obj.fetchone()
            ubal = tup[5]
            uemail = tup[4]
            uname = tup[2]
            con_obj.close()

            if (ubal >= uamt):
                #We also need to check whether the recipient's account exists or not.
                con_obj = sqlite3.connect(database='bank.sqlite')
                cur_obj = con_obj.cursor()

                cur_obj.execute('select * from users where users_acno = ?',(to_acn,))
                con_obj.commit()
                
                tup1 = cur_obj.fetchone()
                con_obj.close()

                if tup1 == None:
                    messagebox.showerror('Transfer Amount','Account does not exist🙄')
                else:
                    to_bal = tup1[5]
                    try:
                        #Generating an OTP for security purposes.
                        otp = random.randint(100000,999999)

                        gmail_con = gmail.GMail(username='bawejaronit164@gmail.com',password='vccs tdjh blrs inni')
                        umsg = f'''Hello {uname}
                                \nWelcome to ABC Bank
                                
                                Your Account No is :- {uacn}
                                Your OTP is :- {otp}

                                Kindly verify the OTP to complete your transaction.
                                
                                Thanks 😊'''
                        
                        msg = gmail.Message(to=uemail,text=umsg,subject='Transaction OTP')
                        gmail_con.send(message=msg)
                        messagebox.showinfo('Transfer Amount','OTP sent!! Kindly check your registered email🌟')
                        uotp=simpledialog.askinteger("OTP","Enter OTP")

                        if (uotp == otp):
                            con_obj = sqlite3.connect(database='bank.sqlite')
                            cur_obj = con_obj.cursor()

                            #Deduct amount from senders bank.
                            cur_obj.execute('update users set users_bal = users_bal - ? where users_acno = ?',(uamt,uacn,))
                            con_obj.commit()

                            #Add amount in receiver's bank.
                            cur_obj.execute('update users set users_bal = users_bal + ? where users_acno = ?',(uamt,to_acn,))
                            con_obj.commit()
                            con_obj.close()

                            #Now we also need to update entries in transactions table.
                            con_obj = sqlite3.connect(database='bank.sqlite')
                            cur_obj = con_obj.cursor()

                                #Firstly insert the record of debit transaction.
                            cur_obj.execute('''insert into txn
                                            (txn_acno,txn_type,txn_date,txn_amt,txn_updatebal)
                                            values(?,?,?,?,?)''',
                                            (uacn,'Db(-)',time.strftime('%d-%b-%d %H:%M:%S %p'),uamt,ubal-uamt))
                            
                            con_obj.commit()
                            
                                #Secondly insert the record of credit transaction.
                            cur_obj.execute('''insert into txn
                                            (txn_acno,txn_type,txn_date,txn_amt,txn_updatebal)
                                            values(?,?,?,?,?)''',
                                            (to_acn,'Cr(+)',time.strftime('%d-%b-%d %H:%M:%S %p'),uamt,to_bal+uamt))
                            
                            con_obj.commit()
                            con_obj.close()

                            messagebox.showinfo('Transaction',f'Amount {uamt} transferred, updated balance {ubal-uamt}')
                            pass
                        else:
                            messagebox.showerror('Transfer Amount','Invalid OTP Entered🥺')
                    except:
                        messagebox.showerror('Transfer','Something Went Wrong😭')
            else:
                messagebox.showerror('Transfer Amount',f'Insufficient balance {ubal}💀')
                amt_entry.delete(0,'end')
            

        #creating a label To_ACN
        to_label = Label(ifrm,text='To ACN',font=('arial',20,'bold'),bg='white',fg='black')
        to_label.place(relx=0.2,rely=0.3)

        #create a to_ACN entry.
        to_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        to_entry.configure(bg='#EED9C4')
        to_entry.place(relx=0.5,rely=0.3)
        to_entry.focus()

        #create an amount label.
        amt_label = Label(ifrm,text='Enter Amount',font=('arial',20,'bold'),bg='white',fg='black')
        amt_label.place(relx=0.2,rely=0.45)

        #create an amount entry.
        amt_entry = Entry(ifrm,font=('arial',20,'bold'),bd=5)
        amt_entry.configure(bg='#EED9C4')
        amt_entry.place(relx=0.5,rely=0.45)

        #Create a transfer button
        transfer_button = Button(ifrm,command=transfer_amt,text='Transfer',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        transfer_button.place(relx=0.5,rely=0.7)

        reset_button = Button(ifrm,command=reset,text='Reset',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5)
        reset_button.place(relx=0.7,rely=0.7)

    def history_click():
        # Creates a frame on parent window,border color->black and border thichness->3pixels.
        ifrm = Frame(frm,highlightbackground='black',highlightthickness=3)
        ifrm.configure(bg='white') #sets frame color to white.
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.65,relheight=0.74) #places frame on parent window frm.

        # Makes a bold heading on derived frame.
        heading_ifrm = Label(ifrm,text='This is View History Screen',font=('Brush Script MT',30,'bold'),bg='white',fg='purple')
        heading_ifrm.pack() #places the label on frame in middle.

        def display_transactions(ifrm):
            """Displays txn history in a formatted Treeview with bold headings and lines."""
            try:
                con = sqlite3.connect('bank.sqlite')
                cursor = con.cursor()

                cursor.execute("SELECT * FROM txn where txn_acno = ?",(uacn,))
                data = cursor.fetchall()
                con.close()

                column_names = [description[0] for description in cursor.description]

                tree = ttk.Treeview(ifrm, columns=column_names, show="headings")

                # Configure style for bold headings and lines
                style = ttk.Style()
                style.configure("Treeview.Heading", font=('TkDefaultFont', 10, 'bold'))  # Bold headings
                style.configure("Treeview", rowheight=25) # Adjust row height for better visibility

                # Set column headings with formatting
                for col in column_names:
                    tree.heading(col, text=col, anchor="center")  # Center headings
                    tree.column(col, width=150, anchor='w', stretch=False)  # Adjust width and prevent stretching
                    
                # Insert data with alternating row colors for better readability
                for i, row in enumerate(data):
                    tree.insert("", "end", values=row, tags=("row",))
                    tree.tag_configure("row", background= "#f0f0f0" if i % 2 == 0 else "white") # Alternating row colors


                # Add separator lines between columns (using canvas)
                def add_separators(event=None):
                    x = 0  # Start at the left edge of the Treeview
                    for col in column_names[:-1]:  # Exclude the last column
                        x += tree.column(col, 'width')
                        tree.canvas.create_line(x, 0, x, tree.winfo_height(), width=1, tags="separator")

                # Add scrollbars
                vsb = ttk.Scrollbar(ifrm, orient="vertical", command=tree.yview)
                vsb.pack(side='right', fill='y')
                tree.configure(yscrollcommand=vsb.set)

                hsb = ttk.Scrollbar(ifrm, orient="horizontal", command=tree.xview)
                hsb.pack(side='bottom', fill='x')
                tree.configure(xscrollcommand=hsb.set)

                tree.pack(fill="both", expand=True)

            except sqlite3.Error as e:
                messagebox.showerror('Txn History', 'Database Error')
                print(f"Database Error: {e}")   #Handle exceptions appropriately.

        display_transactions(ifrm)

    #Welcome user label.
    welcome_label = Label(frm,font=('arial',20,'bold'),text=f"Welcome {uname}",fg='#B10000')   
    welcome_label.place(relx = 0,rely=0)

    #Creating a logout button.
    logout_btn = Button(frm,text='Logout',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=logout_click)
    logout_btn.place(relx=0.90,rely=0.85)

    #Creating a check button.
    check_btn = Button(frm,width=16,text='Check Balance',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=check_click)
    check_btn.place(relx=0,rely=0.1)

    #Creating a update button.
    update_btn = Button(frm,width=16,text='Update Details',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=update_click)
    update_btn.place(relx=0,rely=0.25)

    #Creating a deposit button.
    deposit_btn = Button(frm,width=16,text='Deposit Amount',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=deposit_click)
    deposit_btn.place(relx=0,rely=0.40)

    #Creating a withdraw button
    withdraw_btn = Button(frm,width=16,text='Withdraw Amount',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=withdraw_click)
    withdraw_btn.place(relx=0,rely=0.55)

    #Creating a transfer button
    transfer_btn = Button(frm,width=16,text='Transfer Amount',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=transfer_click)
    transfer_btn.place(relx=0,rely=0.70)

    #Creating a history button
    history_btn = Button(frm,width=16,text='Transaction History',font=('Bookman Old Style',20,'bold'),bg='powder blue',fg='black',bd=5,command=history_click)
    history_btn.place(relx=0,rely=0.85)
    

main_screen()
win.mainloop()