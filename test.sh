# bash script to test an input directory.
# example usage: sh test.sh data/test_LPs_volume2/input/ resutlts/ data/test_LPs_volume2/output/
# WARNING: If using on test_LPs_volume1, the solver will take a LONG TIME on the larger LPs

INPUT_DIR=$1
OUTPUT_DIR=$2
RESULT_DIR=$3

if [ ! -d "$OUTPUT_DIR" ]
then
    mkdir -p "$OUTPUT_DIR"
fi

for f in $INPUT_DIR/*; do
    echo "running on $f"
    filename=$(basename ${f})
    python3 simplex_driver.py < "$f" > "$OUTPUT_DIR/$filename"
    diff "$OUTPUT_DIR/$filename" "$RESULT_DIR/$filename"
done