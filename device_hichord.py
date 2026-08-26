# name=HiChord Pro Engine (MiniLab 3 - 3 Joystick Modes)

import midi
import channels
import device
import ui

# ==========================================
# 1. GLOBAL KEY & SCALE QUANTIZER
# ==========================================
ROOT_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
GLOBAL_ROOT = 0  

SCALES = {
    "MAJOR": [0, 2, 4, 5, 7, 9, 11],
    "MINOR": [0, 2, 3, 5, 7, 8, 10],
    "DORIAN": [0, 2, 3, 5, 7, 9, 10],
    "PHRYGIAN": [0, 1, 3, 5, 7, 8, 10],
    "LYDIAN": [0, 2, 4, 6, 7, 9, 11],
    "MIXOLYDIAN": [0, 2, 4, 5, 7, 9, 10]
}
scale_names_list = list(SCALES.keys())
current_scale_name = "MAJOR"
CURRENT_SCALE = SCALES[current_scale_name]

# MIDI Knob Configuration (CC Values)
CC_KNOB_ROOT = 86   
CC_KNOB_SCALE = 87  
CC_KNOB_OCTAVE = 89
CC_KNOB_INVERSION = 90  
CC_KNOB_BASS = 110  
CC_KNOB_MODE = 111  

GLOBAL_OCTAVE = 0
GLOBAL_INVERSION = 0  
GLOBAL_BASS_MODE = 0  
GLOBAL_JOYSTICK_MODE = 0 # 0: Standard, 1: Extended, 2: Chromatic

# ==========================================
# 2. MODIFIER SYSTEM (8-Way Multi-Mode)
# ==========================================
MODIFIER_KEYS = {
    48: 'up',          
    49: 'up_right',    
    50: 'right',       
    51: 'down_right',  
    52: 'down',        
    53: 'down_left',   
    54: 'left',        
    55: 'up_left'      
}

active_modifier = None
active_chords = {}

def get_diatonic_chord(degree):
    """Calculates chord intervals based on scale and active multi-mode modifiers."""
    root_interval = CURRENT_SCALE[degree]
    third_index = (degree + 2) % len(CURRENT_SCALE)
    third_interval = CURRENT_SCALE[third_index] + (12 if third_index < degree else 0)
    fifth_index = (degree + 4) % len(CURRENT_SCALE)
    fifth_interval = CURRENT_SCALE[fifth_index] + (12 if fifth_index < degree else 0)
    
    rel_third = third_interval - root_interval
    rel_fifth = fifth_interval - root_interval
    
    is_major = rel_third == 4
    is_minor = rel_third == 3
    
    intervals = [0, rel_third, rel_fifth]
    
    if active_modifier:
        # ---------------------------------------------------
        # MODE 0: STANDARD (Base Pop/Rock)
        # ---------------------------------------------------
        if GLOBAL_JOYSTICK_MODE == 0:
            if active_modifier == 'up':
                intervals[1] = 3 if is_major else 4  
            elif active_modifier == 'up_right':
                intervals.append(10)  
            elif active_modifier == 'right':
                intervals.append(11 if is_major else 10)  
            elif active_modifier == 'down_right':
                intervals.append(14)  
            elif active_modifier == 'down':
                intervals[1] = 5  
            elif active_modifier == 'down_left':
                if is_major: intervals.append(9)  
                elif is_minor: intervals[1] = 2  
            elif active_modifier == 'left':
                intervals[1] = 3  
                intervals[2] = 6  
            elif active_modifier == 'up_left':
                intervals[2] = 8  
                
        # ---------------------------------------------------
        # MODE 1: EXTENDED (Richer Jazz & R&B Colors)
        # ---------------------------------------------------
        elif GLOBAL_JOYSTICK_MODE == 1:
            if active_modifier == 'up':
                intervals[1] = 3 if is_major else 4  
            elif active_modifier == 'down':
                intervals = [0, 4, 7, 10, 15] # Dom7#9 (Hendrix crunch)
            elif active_modifier == 'left':
                intervals = [0, 5, 7, 10] # Sus4+7
            elif active_modifier == 'right':
                intervals.append(17) # Add11
            elif active_modifier == 'up_left':
                intervals = [0, 3, 6, 10] # Half-dim7
            elif active_modifier == 'up_right':
                intervals = [0, 4, 7, 10, 14] # Dom9
            elif active_modifier == 'down_left':
                intervals.append(14) # Add9
            elif active_modifier == 'down_right':
                intervals = [0, 3, 7, 10, 17] # Min11
                
        # ---------------------------------------------------
        # MODE 2: CHROMATIC (Advanced Jazz / Altered)
        # ---------------------------------------------------
        elif GLOBAL_JOYSTICK_MODE == 2:
            if active_modifier == 'up':
                intervals = [0, 3, 7, 11] # Min(Maj7) - Film noir
            elif active_modifier == 'down':
                intervals = [0, 4, 7, 11, 14, 21] # Maj13
            elif active_modifier == 'left':
                intervals = [0, 3, 6, 10] # Half-dim7
            elif active_modifier == 'right':
                intervals.extend([9, 14]) # 6/9
            elif active_modifier == 'up_left':
                intervals.extend([11, 18]) # Maj7#11
            elif active_modifier == 'up_right':
                intervals = [0, 4, 7, 10, 14, 21] # Dom13
            elif active_modifier == 'down_left':
                intervals = [0, 4, 7, 10, 13] # Dom7b9 - Spanish dark
            elif active_modifier == 'down_right':
                intervals = [0, 4, 8, 10, 15] # Dom7alt (Alt 5, Alt 9)
        
    return [root_interval + i for i in intervals]

def apply_inversion(notes, inversion_level):
    if not notes or inversion_level == 0:
        return notes
    inverted_notes = sorted(notes.copy())
    actual_inversions = inversion_level % len(inverted_notes)
    for _ in range(actual_inversions):
        lowest = inverted_notes.pop(0)  
        inverted_notes.append(lowest + 12)  
    return inverted_notes

def update_active_chords():
    """Retroactively updates chords with smart note retention (Smooth Blend)"""
    global active_chords
    
    for physical_key, data in list(active_chords.items()):
        playing_notes = data["notes"]
        original_velocity = data["velocity"] 
        
        white_key_mapping = {0:0, 2:1, 4:2, 5:3, 7:4, 9:5, 11:6}
        degree = white_key_mapping[physical_key % 12]
        chord_intervals = get_diatonic_chord(degree)
        
        base_octave = 60 + (GLOBAL_OCTAVE * 12)
        new_notes = [base_octave + GLOBAL_ROOT + interval for interval in chord_intervals]
        new_notes = apply_inversion(new_notes, GLOBAL_INVERSION)
        
        if GLOBAL_BASS_MODE > 0:
            bass_note = base_octave + GLOBAL_ROOT + chord_intervals[0] - (12 * GLOBAL_BASS_MODE)
            new_notes.append(bass_note)
        
        old_notes_set = set(playing_notes)
        new_notes_set = set(new_notes)
        
        notes_to_turn_off = old_notes_set - new_notes_set
        notes_to_turn_on = new_notes_set - old_notes_set
        
        for note in notes_to_turn_off:
            if 0 <= note <= 127:
                channels.midiNoteOn(channels.channelNumber(), note, 0)
                
        for note in notes_to_turn_on:
            if 0 <= note <= 127:
                channels.midiNoteOn(channels.channelNumber(), note, original_velocity)
                
        active_chords[physical_key] = {"notes": list(new_notes), "velocity": original_velocity}

# ==========================================
# 3. MIDI EVENT LISTENERS
# ==========================================

def OnControlChange(event):
    global GLOBAL_ROOT, CURRENT_SCALE, current_scale_name, GLOBAL_OCTAVE, GLOBAL_INVERSION, GLOBAL_BASS_MODE, GLOBAL_JOYSTICK_MODE
    
    print(f"DEBUG [ControlChange] - CC: {event.controlNum} | Value: {event.controlVal}")
    
    if event.controlNum == CC_KNOB_ROOT:
        GLOBAL_ROOT = int((event.controlVal / 127.0) * 11)
        ui.setHintMsg(f"HiChord -> Root: {ROOT_NAMES[GLOBAL_ROOT]} | Scale: {current_scale_name}")
        update_active_chords() 
        event.handled = True

    elif event.controlNum == CC_KNOB_SCALE:
        max_index = len(scale_names_list) - 1
        scale_index = int((event.controlVal / 127.0) * max_index)
        current_scale_name = scale_names_list[scale_index]
        CURRENT_SCALE = SCALES[current_scale_name]
        ui.setHintMsg(f"HiChord -> Root: {ROOT_NAMES[GLOBAL_ROOT]} | Scale: {current_scale_name}")
        update_active_chords()
        event.handled = True
        
    elif event.controlNum == CC_KNOB_OCTAVE:
        new_val = int((event.controlVal / 127.0) * 4.99) - 2 
        if new_val != GLOBAL_OCTAVE:
            GLOBAL_OCTAVE = new_val
            ui.setHintMsg(f"Global Octave: {GLOBAL_OCTAVE}")
            update_active_chords()
        event.handled = True

    elif event.controlNum == CC_KNOB_INVERSION:
        new_val = int((event.controlVal / 127.0) * 3.99)
        if new_val != GLOBAL_INVERSION:
            GLOBAL_INVERSION = new_val
            inversion_names = ["Root Position", "1st Inversion", "2nd Inversion", "3rd Inversion"]
            ui.setHintMsg(f"Inversion: {inversion_names[GLOBAL_INVERSION]}")
            update_active_chords()
        event.handled = True
        
    elif event.controlNum == CC_KNOB_BASS:
        new_val = int((event.controlVal / 127.0) * 2.99)
        if new_val != GLOBAL_BASS_MODE:
            GLOBAL_BASS_MODE = new_val
            bass_states = ["Off", "ON (-1 Oct)", "ON (-2 Oct)"]
            ui.setHintMsg(f"Bass Mode: {bass_states[GLOBAL_BASS_MODE]}")
            update_active_chords()
        event.handled = True

    # NEW: JOYSTICK MODE SELECTOR (CC 111)
    elif event.controlNum == CC_KNOB_MODE:
        new_val = int((event.controlVal / 127.0) * 2.99)
        if new_val != GLOBAL_JOYSTICK_MODE:
            GLOBAL_JOYSTICK_MODE = new_val
            mode_names = ["STANDARD", "EXTENDED", "CHROMATIC"]
            ui.setHintMsg(f"Joystick Mode: {mode_names[GLOBAL_JOYSTICK_MODE]}")
            update_active_chords()
        event.handled = True

def OnNoteOn(event):
    global active_modifier, active_chords, GLOBAL_ROOT
    
    print(f"DEBUG [NoteOn] - MIDI Note: {event.note} | Velocity: {event.velocity}")
    
    # ---------------------------------------------------------
    # ZONA DE MODIFICADORES
    # ---------------------------------------------------------
    if 48 <= event.note <= 59: 
        event.handled = True 
        if event.note in MODIFIER_KEYS:
            active_modifier = MODIFIER_KEYS[event.note]
            update_active_chords() 
        return

    # ---------------------------------------------------------
    # ZONA DE ACORDES
    # ---------------------------------------------------------
    if event.note >= 60:
        white_key_mapping = {0:0, 2:1, 4:2, 5:3, 7:4, 9:5, 11:6}
        note_in_octave = event.note % 12
        
        if note_in_octave not in white_key_mapping:
            event.handled = True 
            return
            
        degree = white_key_mapping[note_in_octave]
        base_octave = 60 + (GLOBAL_OCTAVE * 12)
        
        chord_intervals = get_diatonic_chord(degree)
        final_notes = [base_octave + GLOBAL_ROOT + interval for interval in chord_intervals]
        final_notes = apply_inversion(final_notes, GLOBAL_INVERSION)
        
        if GLOBAL_BASS_MODE > 0:
            bass_note = base_octave + GLOBAL_ROOT + chord_intervals[0] - (12 * GLOBAL_BASS_MODE)
            final_notes.append(bass_note)
        
        for note in final_notes:
            if 0 <= note <= 127:
                channels.midiNoteOn(channels.channelNumber(), note, event.velocity)
                
        active_chords[event.note] = {"notes": final_notes, "velocity": event.velocity}
        event.handled = True

def OnNoteOff(event):
    global active_modifier, active_chords
    
    print(f"DEBUG [NoteOff] - Released MIDI Note: {event.note}")
    
    if 48 <= event.note <= 59:
        event.handled = True
        if event.note in MODIFIER_KEYS and active_modifier == MODIFIER_KEYS[event.note]:
            active_modifier = None
            update_active_chords() 
        return
        
    if event.note in active_chords:
        for note in active_chords[event.note]["notes"]:
            if 0 <= note <= 127:
                channels.midiNoteOn(channels.channelNumber(), note, 0)
        del active_chords[event.note]
        event.handled = True