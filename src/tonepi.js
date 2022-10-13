import * as Tone from 'tone'

const synth = new Tone.MonoSynth().toDestination();

synth.volume.value = 5;

function playSynth(event) {
  Tone.context.resume();
  //console.log(e.target.id);
  let buttonID = event.target.id;
  switch (buttonID) {
    case "button1":
      synth.triggerAttackRelease("C1", "1.5");
      console.log('button 1')
      break;
    case "button2":
      synth.triggerAttackRelease("C2", "1.5");
      console.log('button 2')
      break;
    case "button3":
      synth.triggerAttackRelease("C3", "1.5");
      console.log('button 3')
      break;

    default:
      break;
  }
}

document.getElementById("button1").addEventListener("click", playSynth);

document.getElementById("button2").addEventListener("click", playSynth);

document.getElementById("button3").addEventListener("click", playSynth);
