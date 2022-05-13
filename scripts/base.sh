MACHINES=${MACHINES:-"maps8 maps9 maps10"}
DIR=~/htdocs/carshare
FILE=data.json


##
## scp file to MACHINES if file is of a decent size
##
function scp_file() {
  frm=$1
  to=$2
  s=${3:-11111}

  # check size of data before scp'ing
  size=`ls -ltr $frm | awk -F" " '{ print $5 }'`
  if [[ $size -gt $s ]]
  then
    # scp data
    for m in $MACHINES
    do
      scp="scp $frm $m:$to"
      echo $scp
      eval $scp
    done
  else
    echo "Not SCP'ing $frm (file size $size < $s)"
  fi
}


##
## 1. grab the data using python cmdline app
## 2. scp the file to servers (MACHINES)
## 3. remove the file that was scp'd
##
function run_curl() {
  company=$1
  size=${2:-11111}

  date
  ./bin/$company > $FILE.$company
  scp_file $FILE.$company $DIR/$company/$FILE $size
  rm $FILE.$company
}


# min / hour / month-day / month / weekday

# CARSHARE data updates (see gbfsdb)
# 1 1 * * *    rm carshare.log
# */3 * * * *  source ~/.bashrc; cd ~/gbfsdb; scripts/free2move.sh >> carshare.log 2>&1
# 1 4,13 * * * source ~/.bashrc; cd ~/gbfsdb; scripts/zipcar.sh >> carshare.log 2>&1
