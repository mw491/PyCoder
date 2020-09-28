import logging
import os
import pathlib
import shlex
import shutil
import subprocess
from tkinter import messagebox
from typing import List

log = logging.getLogger(__name__)
_this_dir = pathlib.Path(__file__).absolute().parent
run_script = _this_dir / 'bash_run.sh'


# # # # # # TESTED ONLY ON LINUX # # # # # # #


def run_command(
        blue_message: str, workingdir: pathlib.Path,
        command: List[str]) -> None:
    terminal: str = os.environ.get('TERMINAL', 'x-terminal-emulator')

    # to config what x-terminal-emulator is:
    #
    #   $ sudo update-alternatives --config x-terminal-emulator
    #
    # TODO: document this
    if terminal == 'x-terminal-emulator':
        log.debug("using x-terminal-emulator")

        terminal_or_none = shutil.which(terminal)
        if terminal_or_none is None:
            log.warning("x-terminal-emulator not found")

            # Ellusion told me on irc that porcupine didn't find his
            # xfce4-terminal, and turned out he had no x-terminal-emulator...
            # i'm not sure why, but this should work
            #
            # well, turns out he's using arch, so... anything could be wrong
            terminal_or_none = shutil.which('xfce4-terminal')
            if terminal_or_none is None:
                # not much more can be done
                messagebox.showerror(
                    "x-terminal-emulator not found",
                    "Cannot find x-terminal-emulator in $PATH. "
                    "Are you sure that you have a terminal installed?")
                return

        terminal_path = pathlib.Path(terminal_or_none)
        log.info("found a terminal: %s", terminal_path)

        terminal_path = terminal_path.resolve()
        log.debug("absolute path to terminal: %s", terminal_path)

        # sometimes x-terminal-emulator points to mate-terminal.wrapper,
        # it's a python script that changes some command line options
        # and runs mate-terminal but it breaks passing arguments with
        # the -e option for some reason
        if terminal_path.name == 'mate-terminal.wrapper':
            log.info("using mate-terminal instead of mate-terminal.wrapper")
            terminal = 'mate-terminal'
        else:
            terminal = str(terminal_path)
    else:
        log.debug("using $TERMINAL, it's set to %r" % terminal)

    if shutil.which(terminal) is None:
        messagebox.showerror(
            "%r not found" % terminal,
            "Cannot find %r in $PATH. "
            "Try setting $TERMINAL to a path to a working terminal program."
            % terminal)
        return

    real_command = [str(run_script), blue_message, str(workingdir)]
    real_command.extend(map(str, command))
    subprocess.Popen([terminal, '-e',
                      ' '.join(map(shlex.quote, real_command))])


if __name__ == '__main__':
    run_command("python3", pathlib.Path(), ["python3"])

# old version

# def runfile(event=None):
#     global file
#     if file is None:
#         save = showinfo("Save?", "You have to save your file before running,"
#                                  " Are you sure you want to save now?",
#                         type="okcancel")
#         if save == "ok":
#             file = asksaveasfilename(initialfile='Untitled',
#                                      filetypes=[("Python Files", "*.py"),
#                                                 ("All Files", "*.*"),
#                                                 ("Html Files", "*.html"),
#                                                 ("CSS Files", "*.css"),
#                                                 ("JavaScript Files", "*.js")])
#             if file == "":
#                 file = None
#             else:
#                 window.title(os.path.basename(file) + " - Python PyCode TkEditor")
#                 savedasfile = open(file, "w")
#                 savedasfile.write(textarea.get(1.0, END))
#                 savedasfile.close()
#
#                 if keepconsole.get() == "yes":
#                     os.system(f'gnome-terminal -- sh -c "python3 {file}; bash"')
#                 elif keepconsole.get() == "no":
#                     os.system('"%s"' % f'gnome-terminal -- sh -c "python3 {file};"')
#
#     else:
#         savedfile = open(file, "w")
#         savedfile.write(textarea.get(1.0, END))
#         savedfile.close()
#
#         file_label["text"] = os.path.basename(file)
#
#         if keepconsole.get() == "yes":
#             os.system(f'gnome-terminal -- sh -c "python3 {file}; bash"')
#         elif keepconsole.get() == "no":
#             os.system('"%s"' % f'gnome-terminal -- sh -c "python3 {file};"')
