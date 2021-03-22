# unbmp
makes bitmap images not bitmap images

## Why?
My Nintendo 3DS takes screenshots in `.bmp` format. Some messaging applications that I use do not support embedding or sending `.bmp` files; so I set out to make a shell script to batch convert `bmp`s to `png`. However, I decided that it should handle more input types than `.bmp` and an *If You Give a Mouse a Cookie*-esque cascade of requirements followed. Then I also decided that this would be a good opportunity to learn the `argparse` Python Library; so a simple 5 line shell script morphed into *this*.

## Usage
```
unbmp [-h] [-n] [--verbose] [-d DIRECTORY] [-s SOURCE_EXTENSION]
      [-o OUTPUT_DIRECTORY]
      DEST_EXTENSION [FILE [FILE ...]]

Convert images from one format to another

positional arguments:
  DEST_EXTENSION       file extension for output files
  FILE                 files to convert; mutually exclusive with '-d'

optional arguments:
  -h, --help           show this help message and exit
  -n                   dry run
  --verbose            output debugging text
  -d DIRECTORY         source from a directory
  -s SOURCE_EXTENSION  extension for source filetype; required with -d
  -o OUTPUT_DIRECTORY  output the processed images to a directory
```

## Dependencies

* Wand

This program is Free Software distributed under the MIT License
(c) 2021 bwmabe
