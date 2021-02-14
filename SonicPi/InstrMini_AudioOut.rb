live_loop :esp_note do
  use_real_time
  e_instr, e_note, e_chord = sync "/osc/note"
  
  instrument = :piano if e_instr == 0
  instrument = :chiplead if e_instr == 1
  instrument = :subpulse if e_instr == 2
  instrument = :hoover if e_instr == 3
  
  if e_chord == 0
    synth instrument, note: e_note
  else
    # I - VI - IV - V chord progression
    chord_type = :major7 if e_chord == 1
    chord_type = :minor7 if e_chord == 6
    chord_type = :major7 if e_chord == 4
    chord_type = "7" if e_chord == 5
    synth instrument, note: chord(e_note, chord_type)
  end
end