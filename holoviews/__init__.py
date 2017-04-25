
from __future__ import print_function, absolute_import
import os, sys, pydoc

import numpy as np # noqa (API import)

_cwd = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, os.path.join(_cwd, '..', 'param'))

import param

__version__ = param.Version(release=(1,6,2), fpath=__file__,
                            commit="$Format:%h$", reponame='holoviews')

from .core import archive                                # noqa (API import)
from .core.dimension import OrderedDict, Dimension       # noqa (API import)
from .core.boundingregion import BoundingBox             # noqa (API import)
from .core.options import (Options, Store, Cycle,        # noqa (API import)
                           Palette, StoreOptions)
from .core.layout import *                               # noqa (API import)
from .core.element import *                              # noqa (API import)
from .core.overlay import *                              # noqa (API import)
from .core.tree import *                                 # noqa (API import)
from .core.spaces import (HoloMap, Callable, DynamicMap, # noqa (API import)
                          GridSpace, GridMatrix)

from .interface import *                                             # noqa (API import)
from .operation import ElementOperation, MapOperation, TreeOperation # noqa (API import)
from .element import *                                               # noqa (API import)
from .element import __all__ as elements_list
from . import util # noqa (API import)

# Surpress warnings generated by NumPy in matplotlib
# Expected to be fixed in next matplotlib release
import warnings
warnings.filterwarnings("ignore",
                        message="elementwise comparison failed; returning scalar instead")

try:
    import IPython  # noqa (API import)
    from .ipython import notebook_extension
except ImportError as e:
    class notebook_extension(param.ParameterizedFunction):
        def __call__(self, *args, **opts):
            raise Exception("IPython notebook not available")
    if str(e) != 'No module named IPython':
        raise e


# A single holoviews.rc file may be executed if found.
for rcfile in [os.environ.get("HOLOVIEWSRC", ''),
               "~/.holoviews.rc",
               "~/.config/holoviews/holoviews.rc"]:
    try:
        filename = os.path.expanduser(rcfile)
        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            try:
                exec(code)
            except Exception as e:
                print("Warning: Could not load %r [%r]" % (filename, str(e)))
        break
    except IOError:
        pass


def help(obj, visualization=True, ansi=True, backend=None,
         recursive=False, pattern=None):
    """
    Extended version of the built-in help that supports parameterized
    functions and objects. A pattern (regular expression) may be used to
    filter the output and if recursive is set to True, documentation for
    the supplied object is shown. Note that the recursive option will
    only work with an object instance and not a class.

    If ansi is set to False, all ANSI color
    codes are stripped out.
    """
    backend = backend if backend else Store.current_backend
    info = Store.info(obj, ansi=ansi, backend=backend, visualization=visualization,
                      recursive=recursive, pattern=pattern, elements=elements_list)

    msg = ( "\nTo view the visualization options applicable to this "
            "object or class, use:\n\n"
            "   holoviews.help(obj, visualization=True)\n\n")
    if info:
        print((msg if visualization is False else '') + info)
    else:
        pydoc.help(obj)


def examples(path='holoviews-examples', verbose=False, force=False):
    """
    Copies the notebooks to the supplied path.
    """
    import glob
    from shutil import copytree, ignore_patterns, copyfile

    # A dictionary defining the example files to collect structured
    # into subfolders along with globs and file type extensions
    example_files = {'notebooks': [('../doc/Tutorials/*.{ext}', ('ipynb',))],
                     'assets':    [('../doc/assets/*.{ext}', ('png', 'svg', 'rst'))]}

    packaged_examples = os.path.join(__path__[0], './examples')
    if os.path.exists(packaged_examples) and not force:
        copytree(packaged_examples, path, ignore=ignore_patterns('.ipynb_checkpoints','*.pyc','*~'))
        if verbose:
            print("%s copied to %s" % (source, path))
    else:
        if not os.path.isdir(path): os.mkdir(path)
        for subpath, files in example_files.items():
            subfolder = os.path.join(path, subpath)
            if not os.path.isdir(subfolder): os.mkdir(subfolder)
            for gl, extensions in files:
                file_glob = os.path.join(__path__[0], gl)
                for p in [p for ext in extensions for p in glob.glob(file_glob.format(ext=ext))]:
                    dest = os.path.join(subfolder, os.path.basename(p))
                    copyfile(p, dest)
                    if verbose:
                        print("%s copied to %s" % (p, path))
