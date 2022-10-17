# freeze settings
#brightness 0.5
#blueutil -p 0
#networksetup -setairportpower en0 off

PROJECT_PATH="/Users/mrhmisu/Desktop/styx-server/commons-lang"
DT=`date | tr -d ' :'`
OUT_DIR='/Users/mrhmisu/Repositories/test-smells/energy-profiler/result'
RUN=5
SLEEP=3


# get into the project directory
cd $PROJECT_PATH
# get the list of testclass#testcase from command line arguments
# compile the production code and test
echo "compiling project"
echo "mvn test-compile"
mvn test-compile
echo "waiting for $SLEEP (sec) to cool down..."
sleep $SLEEP

# prepare the PowerLog command
PowerLogger="/Applications/Intel\ Power\ Gadget/PowerLog"

while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "executing' $line"
    for (( i=0; i<RUN; i++ ))
    do
        counter=`expr $i + 1`
        echo "running $line : $counter"
        # prepare the command
        output_file_path="$OUT_DIR/$line-$counter.csv"
        echo $output_file_path
        testcase="-Dtest=\"$line\""
        echo $testcase
        # run the PowerLogger
        /Applications/Intel\ Power\ Gadget/PowerLog -file $output_file_path -cmd mvn test $testcase
        # /Applications/Intel\ Power\ Gadget/PowerLog -file /Users/mrhmisu/Desktop/styx-server/tt.csv -cmd mvn test -Dtest="SimpleEmailTest#testSend"
        echo "waiting for $SLEEP (sec) to cool down..."
        sleep $SLEEP
    done
done <"$1"

# to run
# ./junit-energy-profiler.sh /Users/mrhmisu/Repositories/test-smells/energy-profiler/test-cases.txt