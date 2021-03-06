Generate PDF Title Page with Full Reference and QR Code
=======================================================

A Python script to download the PDFs listed in a bibtex file and generate 1-page
PDF files where containing the title page with the full reference and a QR code
for the download.

Such title pages are nice to put up on blackboards to expose the research of
a lab.

Usage
-----

This git repository should be self contained and work at least on Python 2.7.
Title pages can be generated by invoking the script with a bibtex file as
parameter:

    ./create-front-pages.py references.bib

It will download all PDFs listed as `pdf` in the bibentries. Note that the
bibkey is used for file names. The resulting files are named
`$bibkey.with-ref.pdf`.

License
-------

This code is distributed under the MIT License. Please see the LICENSE file for
details.
