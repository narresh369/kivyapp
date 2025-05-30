#!/bin/bash

echo "Patching gen_gtest_pred_impl.py for Python 3 compatibility..."
GTEST_SCRIPT=".buildozer/android/app/android-sdk/ndk/25.2.9519653/sources/third_party/googletest/scripts/gen_gtest_pred_impl.py"

# Ensure the file exists before modifying
if [[ -f "$GTEST_SCRIPT" ]]; then
    # Convert all print statements not already using parentheses
    sed -i -E "s/^([[:space:]]*)print[[:space:]]+\"(.*)\"/\1print(\"\2\")/" "$GTEST_SCRIPT"
    sed -i -E "s/^([[:space:]]*)print[[:space:]]+'(.*)'/\1print('\2')/" "$GTEST_SCRIPT"
    sed -i -E "s/^([[:space:]]*)print[[:space:]]+([^(\"][^)]*)/\1print(\2)/" "$GTEST_SCRIPT"

    echo "Patch applied to: $GTEST_SCRIPT"
else
    echo "Warning: $GTEST_SCRIPT not found, skipping patch."
fi
