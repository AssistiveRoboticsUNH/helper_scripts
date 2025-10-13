#!/bin/bash
# Automatically find and set the correct sink for your USB audio device.

# Define the base name of the device (part of the sink name)
DEVICE_KEYWORD="usb-Generic_USB2.0_Device"

# Find matching sink from pactl list
SINK_NAME=$(pactl list short sinks | awk -v key="$DEVICE_KEYWORD" '$2 ~ key {print $2}' | head -n 1)

if [ -n "$SINK_NAME" ]; then
    echo "✅ Found sink: $SINK_NAME"
    pactl set-default-sink "$SINK_NAME"
    echo "🔊 Default sink set to: $SINK_NAME"

    # Optional: move all active audio streams to the new sink
    for input in $(pactl list short sink-inputs | awk '{print $1}'); do
        pactl move-sink-input "$input" "$SINK_NAME"
    done
else
    echo "❌ No matching sink found for keyword: $DEVICE_KEYWORD"
    echo "Available sinks:"
    pactl list short sinks
fi
