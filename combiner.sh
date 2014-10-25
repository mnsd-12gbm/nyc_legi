#!/bin/sh
# concatenate all text files in folder without first or last lines

echo "FN Thomson Reuters Web of Science™" >> combined.text

for file in *.txt
do
echo "$file"
tail +2 "$file" | sed '$d' >> combined.text
done

echo "EF" >> comb.text

exit
