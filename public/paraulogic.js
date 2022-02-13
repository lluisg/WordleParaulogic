
async function updatePossiblesValors(){

  lletra = document.getElementById('lletraI').value;
  lletres = document.getElementById('lletres').value;

  if(CheckInput(lletra, lletres)){
    document.getElementById("loading").style.visibility="visible";

    const data = {lletra, lletres};
    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers:{'Content-Type': 'application/json'}
    };
    // const response = await fetch('getDB/'+ exercice +'&'+ unitEx);

    const response = await fetch('/getWords', options);
    const words = await response.json();
    console.log('DB received:');
    console.log(words);

    var text_intro = '';
    var poss_words = '';
    if(words.poss_words.length == 0){
      text_intro = 'Resultats:';
      poss_words = "No hi ha paraules a la nostra base de dades amb aquesta combinació de lletres";
      console.log('No words...');
    }else{
      text_intro = 'Resultats: '+words.poss_words.length+' paraules trobades';
      for(let i=0;i<words.poss_words.length;i++){
        poss_words += words.poss_words[i]+', ';
      };
      console.log(poss_words);
    };

    document.getElementById("loading").style.visibility="hidden";
    document.getElementById("intro").innerHTML = text_intro;
    document.getElementById("paraules").innerHTML = poss_words;

  }else{
    console.log('not valid')
  };
};

function CheckInput(lletra, lletres){

  var lletraValid = true
  var lletresValid = true

  if(lletra.length != 1 || !/^[a-zA-Z]+$/.test(lletra)){
    document.getElementById("lletraI").classList.add('form-control-red');
    document.getElementById("lletraI").classList.remove('text-info');
    document.getElementById("lletraI").classList.add('text-danger');
    document.getElementById("invalid1").style.visibility="visible";
    lletraValid = false
    console.log('not valid 1')
  }else{
    document.getElementById("lletraI").classList.remove('form-control-red');
    document.getElementById("lletraI").classList.remove('text-danger');
    document.getElementById("lletraI").classList.add('text-info');
    document.getElementById("invalid1").style.visibility="hidden";
    console.log('valid 1')
  }

  if(lletres.length == 0 || !/^[a-zA-Z]+$/.test(lletres)){
    document.getElementById("lletres").classList.add('form-control-red');
    document.getElementById("lletres").classList.remove('text-info');
    document.getElementById("lletres").classList.add('text-danger');
    document.getElementById("invalid2").style.visibility="visible";
    lletresValid = false
    console.log('not valid 2')
  }else{
    document.getElementById("lletres").classList.remove('form-control-red');
    document.getElementById("lletres").classList.remove('text-danger');
    document.getElementById("lletres").classList.add('text-info');
    document.getElementById("invalid2").style.visibility="hidden";
    console.log('valid 2')
  }

  if(lletraValid && lletresValid){
    return true
  }else{
    return false
  }
}
