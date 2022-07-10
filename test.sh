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