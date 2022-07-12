# bash script to test an input directory.
# example usage: sh test.sh data/test_LPs_volume2/input/ resutlts/ data/test_LPs_volume2/output/
# WARNING: If using on test_LPs_volume1, the solver will take a LONG TIME on the larger LPs

if [ $# -ne 1 ]
then
     echo "Usage is:"
     echo "sh test.sh [output_directory]"
     exit -1
fi

OUTPUT_DIR=$1

if [ ! -d "$OUTPUT_DIR" ]
then
    mkdir -p "$OUTPUT_DIR"
fi

for dir in 'test_LPs_volume1' 'test_LPs_volume2'; do # data//input/' 'data/test_LPs_volume2/input/'; do
    input_dir="data/$dir/input"
    result_dir="data/$dir/output"

    if [ ! -d "$OUTPUT_DIR/$dir" ]
    then
        mkdir -p "$OUTPUT_DIR/$dir"
    fi

    echo $input_dir
    for f in $input_dir/*; do
        echo "running on $f"
        filename=$(basename ${f})
        python3 simplex_driver.py < "$f" > "$OUTPUT_DIR/$dir/$filename"
        diff "$result_dir/$filename" "$OUTPUT_DIR/$dir/$filename"
    done
done