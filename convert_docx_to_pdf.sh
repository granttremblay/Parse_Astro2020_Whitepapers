#!/bin/bash

# Convert annoying .docx into PDFs
# This requires textutil, which is a Cocoa utility only on macOS (sorry)
# Modified by Grant Tremblay with thanks to an original 
# script by Jacob Salmela
 
for f in "$@"
do
# Get the full file PATH without the extension
filepathWithoutExtension="${f%.*}"
# Convert the DOCX to HTML, which cupsfilter knows how to turn into a PDF
textutil -convert html -output "$filepathWithoutExtension.html" "$f"
# Convert the file into a PDF
cupsfilter "$filepathWithoutExtension.html" > "$filepathWithoutExtension.pdf"
# Remove the temporary HTML file
rm "$filepathWithoutExtension.html" >/dev/null
# Uncomment the following line to remove the original file, leaving only the PDF
# rm "$f" >/dev/null
echo "Word documents (.docx files) have been converted to PDF."
done
