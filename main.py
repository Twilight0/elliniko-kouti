# https://ziimaxx.com/api/operations/accounts/current-lock-data



import sys, os

from tkinter import *
import hashlib
import pyautogui
from greeklish.converter import Converter
import utils, constants


def runner():

    # various helper functions

    def sanitization_level():

        if constants.SANITIZATION_LEVEL == 'ask':

            choices = ['0', '1', '2', '3']
            choice = pyautogui.confirm(text='Which sanitization level do you want?', title='Process Box', buttons=choices)

            if choice is None:

                LEVEL = 0

            else:

                LEVEL = int(choice)

        else:

            LEVEL = int(constants.SANITIZATION_LEVEL)

        return LEVEL

    def greekenglish_prompt():

        if constants.GREEKENGLISH_CONVERSION == 'ask':

            choices = ['yes', 'no', 'reverse']
            choice = pyautogui.confirm(text='Replace english words with greek letters? Or do reverse correction?', title='Process Box', buttons=choices)

            if choice is None:

                result = 'no'

            else:

                return choice

        else:

            result = constants.GREEKENGLISH_CONVERSION

        return result

    # End of various functions

    ws = Tk()
    ws.title("Process Box ")
    ws.option_add('*tearOff', FALSE)

    img = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'icon.png'))

    ws.iconphoto(False, img)
    ws.tk.call('wm', 'iconphoto', ws._w, img)

    if sys.platform == 'linux':

        window_height = 250
        window_width = 180

    else:

        window_height = 200
        window_width = 125

    ws.geometry('{0}x{1}-50-50'.format(window_width, window_height))
    # ws.resizable(False, False)


    def popupresult(s):

        popupRoot = Toplevel(ws)
        popupRoot.title('Process result')
        popupRoot.after(constants.POP_UP_TIMEOUT * 1000, popupRoot.destroy)

        popupButton = Button(popupRoot, text=s, font=("Verdana", 10), bg="yellow", wraplength='550', command=popupRoot.destroy)
        popupButton.pack()

        window_width = 600
        window_height = 65
        # popupRoot.geometry('{0}x{1}-50-50'.format(window_width, window_height))
        popupRoot.geometry('{0}x{1}+670+40'.format(window_width, window_height))
        popupRoot.attributes('-topmost', True)
        popupRoot.update() 

    def notes_box():

        def rClicker(e):

            try:
                def rClick_Copy(e):
                    e.widget.event_generate('<Control-c>')

                def rClick_Cut(e):
                    e.widget.event_generate('<Control-x>')

                def rClick_Paste(e):
                    e.widget.event_generate('<Control-v>')

                def rClick_Selectall(e):
                    e.widget.event_generate('<Control-a>')

                e.widget.focus()

                nclst=[
                    (' Cut', lambda e=e: rClick_Cut(e)),
                    (' Copy', lambda e=e: rClick_Copy(e)),
                    (' Paste', lambda e=e: rClick_Paste(e)),
                    (' Select all', lambda e=e: rClick_Selectall(e))
                    ]

                rmenu = Menu(None, tearoff=0, takefocus=0)

                for (c, (txt, cmd)) in enumerate(nclst):
                    if c == 3:
                        rmenu.add_separator()
                    rmenu.add_command(label=txt, command=cmd)

                try:
                    rmenu.tk_popup(e.x_root+40, e.y_root+10, entry="0")
                finally:
                    rmenu.grab_set()

            except TclError:
                pass

            return "break"

        def select_all(e):
            text_box.tag_add(SEL, "1.0", END)
            text_box.mark_set(INSERT, "1.0")
            text_box.see(INSERT)
            return 'break'

        def new_line_with_numpad(e):
            if sys.platform == 'linux':
                text_box.insert(END, '\n')
            else:
                text_box.insert(END, '\r\n')

        nb_root = Toplevel(ws)
        nb_root.title = ('Notes camvas')

        text_box = Text(nb_root, width=85, height=29, bg="white", font=("Verdana", 16), highlightthickness=1, foreground="black", insertbackground="black", wrap=WORD)
        text_scroll = Scrollbar(nb_root, command=text_box.yview, orient=VERTICAL)
        text_box.config(yscrollcommand=text_scroll.set)

        window_width = 1200
        window_height = 800

        text_scroll.pack(side=RIGHT, fill=Y)

        text_box.focus()
        text_box.pack(side=LEFT, fill=Y)

        text_box.bind('<Button-3>', rClicker, add='')
        text_box.bind("<Control-Key-a>", select_all)
        text_box.bind("<Control-Key-A>", select_all)
        text_box.bind("<KP_Enter>", new_line_with_numpad)
        nb_root.geometry('{0}x{1}+370+40'.format(window_width, window_height))

    # Keep for text box:
    # inp = inputtxt.get(1.0, "end-1c")
    # inputtxt.delete('1.0', 'end')


    def greeklish_converter():

        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, level=sanitization_level())
        myconverter = Converter(max_expansions=4)
        inp = myconverter.convert(inp)[0]
        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def greekenglish_converter():

        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, level=sanitization_level())
        inp = utils.latin2greek(inp, greekenglish_prompt())

        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def greeklish_sanitizer():

        inp = ws.clipboard_get()
        inp = utils.greeklish2greek(inp)

        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)


    def language_conversions():

        choices = ['Convert to greeklish', 'Convert to greek', 'Other conversions']
        choice = pyautogui.confirm(text='Click your choice...', title='Process Box', buttons=choices)

        if choice == 'Convert to greeklish':
            greeklish_converter()
        elif choice == 'Convert to greek':
            greeklish_sanitizer()
        elif choice == 'Other conversions':
            greekenglish_converter()


    def simple_process():

        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, level=sanitization_level())
        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def notes_1():

        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, level=sanitization_level())
        inp = utils.process_for_note(inp, ':\n-')

        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def notes_2():

        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, level=sanitization_level())
        inp = utils.process_for_note(inp, ':')

        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def capitalize():

        inp = ws.clipboard_get()
        inp = utils.strip_accents(inp)
        inp = inp.upper()

        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def sentence():

        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, level=sanitization_level())
        inp = inp.capitalize()

        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def alternating_case():

        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, level=sanitization_level())
        inp = inp.title()

        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def all_lowercase():
        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, level=sanitization_level())
        inp = inp.lower()
        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def change_case():

        choices = ['CAPITALS', 'all lower', 'Sentence', 'Alternative Case']
        choice = pyautogui.confirm(text='Click your choice...', title='Process Box', buttons=choices)

        if choice == 'CAPITALS':
            capitalize()
        elif choice == 'all lower':
            all_lowercase()
        elif choice == 'Sentence':
            sentence()
        elif choice == 'Alternative Case':
            alternating_case()


    def put_into_parenthesis():

        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, dont_change_case=True, level=sanitization_level())
        inp = ''.join(['(', inp, ')'])

        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp


    def fix_notes():

        inp = ws.clipboard_get()
        inp = utils.fix_parenthesis(inp)
        inp = utils.fix_commas(inp)
        inp = utils.fix_abbreviations(inp)
        inp = utils.fix_slashes(inp)
        inp = utils.fix_dashes(inp)

        ws.clipboard_clear()
        ws.clipboard_append(inp)

        popupresult(inp)

        return inp

    def about_notes():

        choices = ['Note with line change', 'Inline note', 'Fix notes', 'Process large notes']
        choice = pyautogui.confirm(text='Click your choice...', title='Process Box', buttons=choices)

        if choice == 'Note with line change':
            notes_1()
        elif choice == 'Inline note':
            notes_2()
        elif choice == 'Fix notes':
            fix_notes()
        elif choice == 'Process large notes':
            notes_box()


    def quotes():

        inp = ws.clipboard_get()
        inp = utils.sanitize(inp, dont_change_case=True, level=sanitization_level())
        inp = ''.join(['"', inp, '"'])
        ws.clip(inp)

        popupresult(inp)

        return inp

    def wrap():

        choices = ['Wrap with quotes', 'Wrap with parenthesis']
        choice = pyautogui.confirm(text='Click your choice...', title='Process Box', buttons=choices)

        if choice == 'Wrap with quotes':
            quotes()
        elif choice == 'Wrap with parenthesis':
            put_into_parenthesis()


    def change_language():
        pyautogui.hotkey('alt', 'shift')


    # def always_on_top():
    #     pyautogui.hotkey('ctrl', 'shift', 'o')


    def remove_decoration():
        pyautogui.hotkey('ctrl', 'shift', 'u')


    # def clear_label():
    #     master_label.config(text='')

    simple_process_button = Button(master=ws, text="Επεξεργασία", command=simple_process, background='gray', fg='white')
    about_notes_button = Button(master=ws, text="Σημείωσεις", command=about_notes, background='white')
    change_case_button = Button(master=ws, text="Αλλαγή μικρά/μεγάλα", command=change_case, background='yellow')
    wrap_button = Button(master=ws, text="Τύλιγμα", command=wrap, background='yellowgreen', fg='black')
    greeklish_button = Button(master=ws, text="Ελληνοαγγλικά", command=language_conversions, background='magenta', fg='white')
    change_language_button = Button(master=ws, text="Αλλαγή γλώσσας", command=change_language, background='skyblue', fg='black')
    # clear_label_button = Button(master=ws, text="Καθαρισμός", command=clear_label, background='red')
    # always_on_top_button = Button(master=ws, text="Πάντα στο προσκήνιο", command=always_on_top, background='green', fg='white')
    remove_decoration_button = Button(master=ws, text="Αφαίρεση του πλαισίου", command=remove_decoration, background='black', fg='white')
    quit_session_button = Button(master=ws, text="Κλείσιμο παραθύρου", command=ws.destroy, background='red', fg='white')
    # countdown_button = Button(master=ws, text="Χρονόμετρο", command=countdown, background='red', fg='white')

    buttons = [
        simple_process_button, change_case_button, about_notes_button,
        wrap_button, greeklish_button, change_language_button,
        quit_session_button
    ]

    if sys.platform == 'linux':

        buttons.insert(-1, remove_decoration_button)

    for b in buttons:

        b.pack()

    if constants.ALWAYS_ON_TOP:
        ws.attributes('-topmost', True)

    return ws


md5sum = u'3f6ad153b3d590399d81d7cf1f482f85'

entered = pyautogui.password(text='Please enter "something"', title='Process Box', default='', mask='*')

if entered is None:
    pyautogui.alert('Something wrong happened', 'Process box prompt', timeout=5 * 1000)
    try:
        raise KeyboardInterrupt
    except KeyboardInterrupt:
        sys.exit()

try:
    md5_conversion = hashlib.md5(entered).hexdigest()
except TypeError:
    md5_conversion = hashlib.md5(bytes(entered, encoding='utf-8')).hexdigest()

passed =  md5sum == md5_conversion

if passed:

    ws = runner()

    try:
        

        if constants.ALWAYS_ON_TOP:
            ws.update()
        ws.mainloop()
    
    except KeyboardInterrupt:

        ws.destroy()

else:

    try:
        pyautogui.alert('Something wrong happened', 'Process box prompt', timeout=5 * 1000)
        raise KeyboardInterrupt
    except KeyboardInterrupt:
        sys.exit()
