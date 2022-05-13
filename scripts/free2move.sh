MACHINES="maps8 maps9 maps10"
DIR=~/htdocs/carshare/free2move
FILE=data.json

# curl data
./bin/free2move > $FILE.ftm

# scp data
for m in $MACHINES
do
  scp="scp $FILE.ftm $m:$DIR/$FILE"
  echo $scp
  eval $scp
done
