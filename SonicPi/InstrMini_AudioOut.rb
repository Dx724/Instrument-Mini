live_loop :esp_note do
  use_real_time
  e_instr, e_note = sync "/osc/note"
  
  synth :piano, note: e_note if e_instr == 0
  synth :chiplead, note: e_note if e_instr == 1
  synth :blade, note: e_note if e_instr == 2
  synth :hoover, note: e_note if e_instr == 3
end