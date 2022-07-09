INPUT_DIR=$1
OUTPUT_DIR=$2

if [[ ! -d "$OUTPUT_DIR" ]]
then
    echo "Did not exist"
    mkdir -p "$OUTPUT_DIR"
fi

for f in $INPUT_DIR/*; do
    filename=$(basename ${f})
    python3 simplex_driver.py < "$f" > "$OUTPUT_DIR/$filename"
done