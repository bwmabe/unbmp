#!/usr/bin/env python3

import argparse
import os
import sys
import typing
import wand  # type: ignore
from wand.image import Image  # type: ignore

# Global Flags
VERBOSE = False
DRY_RUN = False


def check_filetype(fname: str, ftype: str) -> bool:
    """Check if a file is of the desired type

    Arguments:
    fname -- the filename
    ftype -- the desired filetype
    """

    if os.path.isdir(fname):
        return False
    if len(fname) < len(ftype):
        return False
    return fname[-(len(ftype) + 1):].lower() == '.' + ftype.lower()


def get_conv_fname(fname: str, dest_ext: str, output_dir=None) -> str:
    """Returns the filename and path of the file after conversion

    Arguments:
    fname -- the original filename
    dest_ext -- the extension of the destination file
    output_dir -- the output directory of the operation
    """

    if output_dir is not None:
        fname_wo_path = fname.split('/')[-1][:-4] + '.' + dest_ext
        if output_dir[-1] != '/':
            output_dir = output_dir + '/'
        return output_dir + fname_wo_path
    else:
        return fname[:-4] + '.' + dest_ext


def concat_filename(path: str, fname: str) -> str:
    """Concatenates the source filename and source path

    Arguments:
    path -- the path of the file
    fname -- the filename
    """

    if path[-1] != "/":
        return path + "/" + fname
    else:
        return path + fname


def convert(files: typing.List[str], dest_ext: str, src_ext=None,
            output_dir=None) -> None:
    """Converts a list of files to a different filetype
    Optionally puts them in a desired directory

    Arguments:
    files -- a List of files to be converted
    dest_ext -- the file extension to convert to
    src_ext -- the extension of files to be converted
    output_dir -- (optional) the directory in which the output files are placed
    """

    ext = ""
    to_convert = []
    converted = 0
    failed = []

    if src_ext is None:
        ext = "bmp"
    else:
        ext = src_ext

    for fname in files:
        if check_filetype(fname, ext):
            conv_fname = get_conv_fname(fname, dest_ext, output_dir)
            to_convert.append((fname, conv_fname))

    if DRY_RUN:
        if to_convert:
            print("To Modify:")
            for i in to_convert:
                print("%s -> %s" % i)
            print("{} files will be modified".format(len(to_convert)))
        else:
            print("Nothing to change")
        return

    for i in to_convert:
        if VERBOSE:
            print("%s -> %s" % i)

        try:
            with Image(filename=i[0]) as img:
                img.format = dest_ext
                img.save(filename=i[1])
                converted += 1
                if VERBOSE:
                    print("Converting {} succeeded".format(i[0]))
        except wand.exceptions.CorruptImageError:
            print("'{}' is not a {} image".format(i[0], src_ext))
            failed.append(i[0])
        except Exception as e:
            print(e)
            failed.append(i[0])

    if VERBOSE:
        if failed:
            print("{} image(s) processed; {} converted; {} failed"
                  .format(len(to_convert), converted, len(failed)))
        else:
            print("all {} images converted".format(len(to_convert)))


def find_images(directory: str, dest_ext: str, src_ext=None,
                output_dir=None) -> None:
    """Examines a directory and returns images that can be converted

    Arguments:
    directory -- the directory to look for files in
    dest_ext -- the extension that files should ahve after conversion
    src_ext -- the extension of files to be converted
    output_dir -- the directory to output converted files to
    """

    dir_contents = os.listdir(directory)
    to_convert = []
    ext = ""

    if src_ext is None:
        ext = "bmp"
    else:
        ext = src_ext

    for fname in dir_contents:
        if check_filetype(fname, ext):
            if VERBOSE:
                print("Found '{}'".format(fname))
            to_convert.append(concat_filename(directory, fname))

    if to_convert:
        if VERBOSE:
            print("{} files found".format(len(to_convert)))
        convert(to_convert, dest_ext, src_ext, output_dir)
    else:
        print("Nothing Found")


def main(argv: list) -> None:
    """ Handles argument parsing and input validation

    Arguments:
    argv -- a list of arguments
    """

    global VERBOSE
    global DRY_RUN

    parser = argparse.ArgumentParser(
        description='Convert images from one format to another')

    parser.add_argument('-n', action='store_true',  help='dry run')

    parser.add_argument('--verbose', action='store_true',
                        help='output debugging text')

    parser.add_argument('output_extension', metavar='DEST_EXTENSION', type=str,
                        help="file extension for output files")

    parser.add_argument('-d', metavar='DIRECTORY', type=str,
                        help="source from a directory", required=False)

    parser.add_argument('-s', metavar='SOURCE_EXTENSION', type=str,
                        help="extension for source filetype; required with -d")

    parser.add_argument('-o', metavar='OUTPUT_DIRECTORY', type=str,
                        help="output the processed images to a directory")

    parser.add_argument('input_files', metavar='FILE', type=str, nargs='*',
                        help="files to convert; mutually exclusive with '-d'")

    args = parser.parse_args(argv)

    VERBOSE = args.verbose
    DRY_RUN = args.n

    if args.d is not None:
        if args.input_files:
            print("unbmp: error: DIRECTORY and FILEs are mutually exclusive")
            exit(1)

        if args.s is None:
            print("unbmp: error: '-s' is required when '-d' is used")
            exit(1)

        find_images(args.d, args.output_extension, args.s, args.o)
    else:
        if not args.input_files:
            print("unbmp: error: input FILES are required if '-d' is not used")
            exit(1)

        convert(args.input_files, args.output_extension, args.s, args.o)


if __name__ == "__main__":
    main(sys.argv[1:])

# vi:syntax=python
