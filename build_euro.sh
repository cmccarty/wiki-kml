#!/bin/sh

OUT="euro_2016-2.txt"
KML="europe_2016.kml"

echo "## Europe" > $OUT
cat misc_europe.txt >> $OUT
cat austria.txt >> $OUT
cat belgium.txt >> $OUT
cat czech_republic.txt >> $OUT
cat germany.txt >> $OUT
cat hungary.txt >> $OUT
cat netherlands.txt >> $OUT


python wiki_kml.py -i $OUT -o $KML