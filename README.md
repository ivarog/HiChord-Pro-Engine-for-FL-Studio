# HiChord Pro Engine for FL Studio
_Created by Ivan Aco_

A custom Python MIDI script that transforms the Arturia MiniLab 3 (or any MIDI controller) into a smart, real-time chord generator and arranger, heavily inspired by the HiChord hardware.

This script allows you to generate diatonic chords with a single key press, dynamically alter their musical qualities using a multi-bank pad modifier system, and tweak voicings, octaves, and bass notes in real-time using endless encoders.

---

## 🚀 Features

* **One-Finger Diatonic Chords:** Pressing any white key starting from C5 (MIDI note 60) triggers a full, harmonically correct chord based on your currently selected global scale and root note.
* **Global Scale & Root Quantizer:** Change the harmonic foundation of your entire project on the fly without menu diving. Supported scales: Major, Minor, Dorian, Phrygian, Lydian, and Mixolydian.
* **3 Joystick Modes (24 Live Modifiers):** Use your drum pads like a multi-bank joystick. Depending on the selected mode (Standard, Extended, or Chromatic), you can inject 24 different real-time chord alterations—from simple Sus4s to complex Jazz and R&B voicings (like Dom7#9 or 13ths)—while holding a chord.
* **Automatic Voice Leading (Inversions):** Cycle through chord inversions (Root, 1st, 2nd, 3rd) to ensure smooth, professional-sounding transitions between chords, minimizing awkward frequency jumps.
* **Bass Mode:** Automatically injects a deep bass note (the root of the chord) one or two octaves below the current voicing to create massive, full-sounding progressions without using your left hand.
* **Velocity Inheritance:** Modifiers and real-time tweaks seamlessly inherit the exact MIDI velocity of your original key press, preserving human feel and dynamics.
* **Native UI Integration:** Visual feedback is natively integrated into FL Studio's Hint Panel. Every knob turn or pad press displays your current Root, Scale, Octave, Inversion, Bass, and Joystick state.

---

## 🎛️ Control Encoders (Knobs)

The engine utilizes FL Studio's `OnControlChange` event to listen to specific Control Change (CC) values. Map your endless encoders to the following CC numbers:

| CC Number | Function | Description | Range / Options |
| :--- | :--- | :--- | :--- |
| **CC 86** | Global Root Note | Shifts the base key of the diatonic engine. | C, C#, D, D#, E, F, F#, G, G#, A, A#, B |
| **CC 87** | Global Scale | Changes the interval structure of the white keys. | Major, Minor, Dorian, Phrygian, Lydian, Mixolydian |
| **CC 89** | Global Octave | Shifts the output up or down in octaves. | -2, -1, 0, +1, +2 |
| **CC 90** | Chord Inversions | Rearranges the notes for smooth voice leading. | Root Position, 1st, 2nd, 3rd Inversion |
| **CC 110** | Bass Mode | Adds a root bass note below the chord. | Off, -1 Octave, -2 Octaves |
| **CC 111** | Joystick Mode | Switches the active bank for the modifier pads. | Standard, Extended, Chromatic |

---

## 🕹️ The "Joystick" Modifiers (Pads)

Map your 8 drum pads to MIDI notes **48 through 55**. Pressing these pads while holding a chord will instantly transform it based on your current **Joystick Mode (CC 111)**.

### Mode 0: STANDARD (Pop / Rock / Foundation)
*Focuses on the most common diatonic alterations.*

| Pad Freq / MIDI | Direction | Result / Vibe | What Changes (Theory) |
| :--- | :--- | :--- | :--- |
| **48** | ⬆️ Up | **Maj ↔ Min** | Flips the 3rd to change the chord's emotional character. |
| **49** | ↗️ Up-Right | **Bluesy** | Adds a flatted 7th note (Dom7). |
| **50** | ➡️ Right | **Jazzy** | Adds the natural 7th (Maj7 / min7). |
| **51** | ↘️ Down-Right| **Lush** | Adds the 9th for a modern, colorful sound. |
| **52** | ⬇️ Down | **Open** | Replaces the 3rd with the 4th (Sus4). |
| **53** | ↙️ Down-Left | **Sweet** | Adds 6th on major chords / replaces 3rd with 2nd (Sus2) on minor. |
| **54** | ⬅️ Left | **Dark** | Lowers the 3rd and 5th to force a Diminished chord (Maximum darkness). |
| **55** | ↖️ Up-Left | **Dreamy** | Raises the 5th by a half step (Augmented). |

### Mode 1: EXTENDED (Richer Jazz & R&B Colors)
*Focuses on adding color notes without losing the base structure.*

| Pad Freq / MIDI | Direction | Result / Vibe | What Changes (Theory) |
| :--- | :--- | :--- | :--- |
| **48** | ⬆️ Up | **Maj ↔ Min** | Flips bright/dark (same as standard). |
| **49** | ↗️ Up-Right | **Dom9** | Adds flat 7th + 9th. Smooth funk. |
| **50** | ➡️ Right | **Add11** | Adds the 11th (4th up an octave). Open, modern. |
| **51** | ↘️ Down-Right| **Min11** | Minor chord + flat 7th + 11th. Modal, open. |
| **52** | ⬇️ Down | **Dom7#9** | Adds flat 7th AND sharp 9th. Hendrix crunch tension. |
| **53** | ↙️ Down-Left | **Add9** | Adds the 9th without a 7th. Warm sparkle. |
| **54** | ⬅️ Left | **Sus4+7** | Replaces 3rd with 4th, adds flat 7th. Suspended tension. |
| **55** | ↖️ Up-Left | **Half-dim7** | Lowers 3rd, lowers 5th, adds flat 7th. Bittersweet. |

### Mode 2: CHROMATIC (Advanced Jazz / Altered Dominants)
*Focuses on high-tension, cinematic, and complex voicings.*

| Pad Freq / MIDI | Direction | Result / Vibe | What Changes (Theory) |
| :--- | :--- | :--- | :--- |
| **48** | ⬆️ Up | **Min(Maj7)** | Minor chord + natural 7th. Film noir / dramatic. |
| **49** | ↗️ Up-Right | **Dom13** | Flat 7th + 9th + 13th. Rich tension. |
| **50** | ➡️ Right | **6/9** | Adds both the 6th and 9th. Smooth jazz landing. |
| **51** | ↘️ Down-Right| **Dom7alt** | Flat 7th + altered 5th + altered 9th. Maximum spice. |
| **52** | ⬇️ Down | **Maj13** | Stacks the 7th, 9th, and 13th. Full, warm. |
| **53** | ↙️ Down-Left | **Dom7b9** | Flat 7th + flatted 9th. Spanish, dark tension. |
| **54** | ⬅️ Left | **Half-dim7** | Lowers 3rd & 5th, adds flat 7th. Dark jazz. |
| **55** | ↖️ Up-Left | **Maj7#11** | Adds natural 7th + raised 11th. Ethereal, Lydian flavor. |

---

## 🛠️ Installation

1. Open FL Studio.
2. Navigate to your FL Studio User Data folder: `Documents\Image-Line\FL Studio\Settings\Hardware`.
3. Create a new folder named `HiChord_Engine`.
4. Drop the `device_hichord.py` script into this folder.
5. In FL Studio, open **Options > MIDI Settings**.
6. Select your Arturia MiniLab 3 from the Input list.
7. In the "Controller type" dropdown menu, find and select **HiChord Pro Engine**.
8. Enable the controller and enjoy!

## 🐛 Debugging & Mapping

The script includes built-in console logging. To view real-time MIDI data (useful for mapping new knobs or troubleshooting controller inputs):
1. In FL Studio, go to the top menu: **View > Script output**.
2. Any pressed key, pad, or turned encoder will print its exact `MIDI Note` or `CC Value` directly to the console. Update the CC variables at the top of the script if your knobs do not match the defaults.