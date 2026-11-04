"""DuraPy Examples - UniCLI interactive REPL.

Run this script to launch the DuraPy shell, or use the console script::

    durapy

Try::

    mach_number 340
    slope 0 0 2 4
    :again 680
    last(680)
"""

from durapy.uniCLI.repl import DuraPyREPL

if __name__ == "__main__":
    DuraPyREPL().run()
