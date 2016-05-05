File List Expansion - flist
===

With `flist` you can express a long list of files using a concise description. It can be used both
as a module and as a command line utility.

Installation
---

There several options for installing `flist`:

- Copy the file `flist.py` to your project. It is just a single file with no dependencies. Or,

- Install using `pip install flist`. Or,

- Clone the project from GitHub - `git clone https://github.com/avnr/flist`. Or,

- Download from GitHub the latest release in your preferred format - `https://github.com/avnr/flist/releases`. Or,

- Download from GitHub the tarball - `wget --no-check-certificate https://github.com/avnr/flist/archive/0.7.tar.gz`.

Requires Python3. Import with `from flist import flist` or `from flist import iflist`.

Calling `flist`
---

- **Basic Call** - `flist` accepts a name and finds all matching files. E.g., if file `foo` exists,
`flist("foo")` will return `["/full/path/to/foo"]`, otherwise it will return `[]`.

- **Expand Directories** - If `foo` is a directory, and the `recurse` flage is set, `flist("foo",
recurse=True)` will return a list of all files in the directory, and will recurse into other
directories that may be inside it. By default the `recurse` flag is `False`.

- **Expand Wildcards** - Names are expanded with globbing, e.g., `flist("bar/foo.*")` will expand
simillar to globbing in a shell, including the globing of `?` and `[]`, and return a list of all
existing, matching file names. `flist("*")` will not expand filenames beginning with a period. To
expand these, specify the period explicitly.

- **Expand Evironment Variables** - You can specify file names using environment variables as in
`flist("$MYAPP_HOME/foo")` and `flist("${MYAPP_HOME}/foo")`. On Windows you can also use
`flist("%MYAPP_HOME%/foo")`.

- **Expand Home Directory** - The tilde sign will be replaced by the user's home directory as in
`flist("~/foo")` and `flist("~user/foo")`.

- **Search in Path** - You can specify a path to search, and `flist` will apply it to any file
names that have no path portion and not otherwise matched. So if in the current working directory
there's no such file `foo`, `flist("foo", path=sys.path)` will search for foo in `sys.path`, and
will return all files called `foo` and (if `recurse=True`) all files in all directories called
`foo` under any directory that appears in the path. For `flist("bar/foo", path=sys.path)`, if file
`bar/foo` doesn't exist then `flist` won't search for it in the path because the file path has been
explicitly specified.

- **Reference Files** - You can create a reference file that will contain a list of files to match,
and provide it to `flist` prefixed by an at sign: `flist("@foo")` will look for file `foo`; it is
expected that each non-empty line in the file `foo` will specify a file name to match according to
all of the above rules. The paths of referenced files are relative to the path of the referencing
file. The reference file can be commented by placing a hastag - `#` - before the comment. You can
also specify inside the reference file another reference, using the same notation; just beware
self-references - `flist` doesn't check for recursions! Note that specifying a path argument doesn't
effect reference files lookup (but it does on the referenced files). Also note that reference
files must exist and are not globbed, specifying a non-existant reference file will raise an
exception. `flist` will return only unique file names even if they are referenced more than once.

- **Expanding a List** - You can call `flist` with a list of file names, e.g.
`flist(["foo","@bar","baz"])` with or without a path argument. Every file name can be specified
using all of the above options. `flist` will return only unique file names even if a file name
matchs more than one pattern.

- **Using Callbacks** - You can supply `flist` a callback, and `flist` will iterate without storing
the entire list of file names, calling the callback for each name. Note when using a callback that
because `flist` will not keep the list of already-visited names, the callback might be called more
than once with the same file name. Example:

        def cb(filename):
            # do something with file name

        flist("*.conf", cb=cb)

- **Using as Iterator** - You can also use the `iflist` iterator to iterate over all file names. As
with callbacks, `iflist` won't store the list of file names already found, so the same file name
might be generated more than once. Example:

        for filename in iflist("*.conf"):
            # do something with filename

CLI Usage
---

You can call `flist` from the command line with one or more file names to expand, using all file
name options. The `flist` utility automatically applies sys.path as the path argument. You can
modify the path using the -n option (use no path), or the -p &lt;path&gt; option (use an
alternative path separated by commas or semicolons). It is not possible to specify a callback. The
utility will print to stdout a whitespace separated list of double-quoted resulting file names.
Example:

    $ flist foo bar
    "/path/to/foo" "/path/to/bar"

For the utility to recurse into directories use the -r option.

By default the utility uses the non-iterator call `flist` and returns only unique names. If your
list is very long you can specify the -i option which will instead invoke the `iflist` iterator
which is more efficient, however it may return duplicate results if the same file name matches more
than one pattern.

To get a list of all options use the -h option.

License
---

MIT License

Release Notes
---

0.7, May 5, 2016:

- flist will now return all files including directories (except when directories will be expanded if
recursion was requested)

- Styling & typos

0.602, October 26, 2015:

- Fixed version notation

0.601, October 21, 2015:

- Fixed __init__ so that it works well when installed through Pypi

- Added a __main__ file so that `flist` can be invoked from CLI using `python -m flist`

- Moved expansion of tilde (user home) and environment variables so that they work well also for
reference files.

