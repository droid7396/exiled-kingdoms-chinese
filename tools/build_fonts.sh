#!/bin/bash
set -e
TOOLS="C:/Games/Exiled Kingdoms-build11985424/_tools"
ZH="C:/Games/Exiled Kingdoms-build11985424/_zh"
OUT="$ZH/data/ui/fonts"
FONT="C:/Games/Exiled Kingdoms-build11985424/_tools/WQYMicroHeiEK.ttf"
CHARS="$TOOLS/chars_all.txt"
TMP="$ZH/gen"

mkdir -p "$TMP" "$OUT"

declare -A sizes=( [default]=15 [tahoma16white]=14 [tahoma20bold]=18 [tahoma20white]=18   [tahoma22bold]=20 [tahoma22outline]=20 [tahoma23white]=21 [tahoma24bold]=22 [tahoma25white]=23   [tahoma26bold]=24 [tahoma27bold]=25 [tahoma27outline]=25 [tahoma27white]=25 [tahoma31outline]=29   [tahoma32]=30 [tahoma32bold]=30 [tahoma38outline]=36 [arialnarrow40bold]=38 )

# 1. one bitmap font per unique pixel size (incremental: skips existing)
for s in $(printf '%s\n' "${sizes[@]}" | sort -un); do
  if [ -s "$TMP/size$s.fnt" ]; then echo "== size $s already done"; continue; fi
  echo "== generating size $s ($(date +%H:%M:%S))"
  (cd "$TOOLS" && ./fontbm.exe --font-file "$FONT" --font-size $s \
    --chars-file "$CHARS" \
    --output "$TMP/size$s" --data-format txt \
    --texture-size 2048x2048,4096x4096) 2>&1 | grep -v "not found" || true
  [ -s "$TMP/size$s.fnt" ] || { echo "FAILED size $s"; exit 1; }
done

# 2. derive each target font from its size template (temp file + move, no in-place sed)
for name in "${!sizes[@]}"; do
  s=${sizes[$name]}
  pages=$(grep -c '^page' "$TMP/size$s.fnt")
  for ((p=0; p<pages; p++)); do
    cp "$TMP/size${s}_${p}.png" "$OUT/${name}_${p}.png"
  done
  sed "s/size${s}_/${name}_/g" "$TMP/size$s.fnt" > "$TMP/${name}.tmp"
  mv "$TMP/${name}.tmp" "$OUT/${name}.fnt"
  echo "built $name (size $s, $pages pages)"
done

echo ALL_DONE
