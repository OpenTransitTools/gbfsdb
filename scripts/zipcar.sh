MACHINES="maps8 maps9 maps10"
DIR=~/htdocs/carshare/zipcar
FILE=data.json

# curl data
./bin/zipcar > $FILE.zip

# scp data
for m in $MACHINES
do
  scp="scp $FILE.zip $m:$DIR/$FILE"
  echo $scp
  eval $scp
done
