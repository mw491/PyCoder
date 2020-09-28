import tkinter as tk


def comment_or_uncomment(textwidget):
    try:
        start_index, end_index = map(str, textwidget.tag_ranges('sel'))
    except ValueError:
        # nothing selected, add '#' normally
        return None

    start = int(start_index.split('.')[0])
    end = int(end_index.split('.')[0])
    if end_index.split('.')[1] != '0':
        # something's selected on the end line, let's (un)comment it too
        end += 1

    gonna_uncomment = all(
        textwidget.get('%d.0' % lineno, '%d.1' % lineno) == '#'
        for lineno in range(start, end))

    for lineno in range(start, end):
        if gonna_uncomment:
            textwidget.delete('%d.0' % lineno, '%d.1' % lineno)
        else:
            textwidget.insert('%d.0' % lineno, '#')

    # select everything on the (un)commented lines
    textwidget.tag_remove('sel', '1.0', 'end')
    textwidget.tag_add('sel', '%d.0' % start, '%d.0' % end)
    return 'break'


# if __name__ == '__main__':
#     w = tk.Tk()
#     t = tk.Text(w)
#     t.pack()
#     t.bind("<Control-slash>", lambda e: comment_or_uncomment(t))
#
#     w.mainloop()


pop_os = '''
                                            ,---,  
,-.----.                                 ,`--.' |  
\    /  \                                |   :  :  
|   :    \           ,-.----.            '   '  ;  
|   |  .\ :   ,---.  \    /  \           |   |  |  
.   :  |: |  '   ,'\ |   :    |          '   :  ;  
|   |   \ : /   /   ||   | .\ :          |   |  '  
|   : .   /.   ; ,. :.   : |: |          '   :  |  
;   | |`-' '   | |: :|   |  \ :          ;   |  ;  
|   | ;    '   | .; :|   : .  |          `---'. |  
:   ' |    |   :    |:     |`-'      ___  `--..`;  
:   : :     \   \  / :   : :      .'  .`|.--,_     
|   | :      `----'  |   | :   .'  .'   :|    |`.  
`---'.|              `---'.|,---, '   .' `-- -`, ; 
  `---`                `---`;   |  .'      '---`"  

'''

print(pop_os)
