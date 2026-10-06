#!/bin/bash
set -e
TOOLS="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$TOOLS")"
OUT="${1:-$ROOT/fonts_out}"
FONT="${FONT:-/c/Windows/Fonts/simhei.ttf}"
FONTBM="$ROOT/fontbm/fontbm.exe"
CHARS="$TOOLS/chars_all.txt"
TMP="$ROOT/gen"

mkdir -p "$TMP" "$OUT"

declare -A sizes=( [default]=17 [tahoma16white]=16 [tahoma20bold]=20 [tahoma20white]=20 [tahoma22bold]=22 [tahoma22outline]=22 [tahoma23white]=23 [tahoma24bold]=24 [tahoma25white]=25 [tahoma26bold]=26 [tahoma27bold]=27 [tahoma27outline]=27 [tahoma27white]=27 [tahoma31outline]=31 [tahoma32]=32 [tahoma32bold]=32 [tahoma38outline]=38 [arialnarrow40bold]=40 )

# 1. one bitmap font per unique pixel size (incremental: skips existing)
for s in $(printf '%s\n' "${sizes[@]}" | sort -un); do
  if [ -s "$TMP/size$s.fnt" ]; then echo "== size $s already done"; continue; fi
  echo "== generating size $s ($(date +%H:%M:%S))"
  (cd "$ROOT/fontbm" && ./fontbm.exe --font-file "$FONT" --font-size $s \
    --chars-file "$CHARS" \
    --output "$TMP/size$s" --data-format txt \
    --texture-size 2048x2048,4096x4096) 2>&1 | grep -v "not found" || true
  [ -s "$TMP/size$s.fnt" ] || { echo "FAILED size $s"; exit 1; }
done

# 2. derive each target font from its size template; fnt must be CRLF for the game
for name in "${!sizes[@]}"; do
  s=${sizes[$name]}
  pages=$(grep -c '^page' "$TMP/size$s.fnt")
  for ((p=0; p<pages; p++)); do
    cp "$TMP/size${s}_${p}.png" "$OUT/${name}_${p}.png"
  done
  sed -e "s/size${s}_/${name}_/g" -e 's/$/\r/' "$TMP/size$s.fnt" > "$OUT/${name}.fnt"
  echo "built $name (size $s, $pages pages)"
done

echo ALL_DONE
