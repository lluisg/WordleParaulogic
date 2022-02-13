var list_all5_global = []

function nextInput(pos){
  pos_next = parseInt(pos)+1;
  id_next = "lletra"+pos_next.toString();
  col = id_next.slice(-1)
  row = id_next.slice(-2, -1)

  if(col == '6'){
    document.getElementById('seguent'+row).style.visibility = "visible";
  }else{
    document.getElementById(id_next).focus();

  };
};

function ResultatLletra(lletra, res){
  id_lletra = 'lletra'+lletra
  if(res == 'C'){
    document.getElementById(id_lletra).classList.add('bg-success')
    document.getElementById(id_lletra).classList.remove('bg-warning')
    document.getElementById(id_lletra).classList.remove('bg-danger')
    document.getElementById(id_lletra).classList.remove('text-info')
  }else if(res == 'M') {
    document.getElementById(id_lletra).classList.remove('bg-success')
    document.getElementById(id_lletra).classList.add('bg-warning')
    document.getElementById(id_lletra).classList.remove('bg-danger')
    document.getElementById(id_lletra).classList.remove('text-info')
  }else if(res == 'I'){
    document.getElementById(id_lletra).classList.remove('bg-success')
    document.getElementById(id_lletra).classList.remove('bg-warning')
    document.getElementById(id_lletra).classList.add('bg-danger')
    document.getElementById(id_lletra).classList.remove('text-info')
  }
}

async function makeNextSuggerencia(torn){
  var checked = await CheckWordInput(torn)
  if(checked){
    console.log('es correcte?', checked)
    document.getElementById('seguent'+torn).style.visibility = "hidden";
  }else{
    console.log('no es una de les paraules que tenim possibles')
  }
}

async function CheckWordInput(torn){
  console.log('listall5', list_all5_global.length);
  var paraula = "";
  var paraula_valida = true;
  for(let i=1; i<=5; i++){
    inputname = "lletra"+torn+i;
    let lletra = document.getElementById(inputname).value;
    if(/^[a-zA-Z]+$/.test(lletra)){
      paraula += lletra;
    }else{
      paraula_valida = false;
      break;
    }
  }
  paraula = paraula.toUpperCase();
  console.log('paraula input', paraula, paraula_valida);

  if(paraula_valida){
    if(list_all5_global.length < 1){
      const data = {};
      const options = {
        method: 'POST',
        body: JSON.stringify(data),
        headers:{'Content-Type': 'application/json'}
      };
      const response = await fetch('/getAll5', options);
      list_all5_response = await response.json();
      console.log('DB received:');
      console.log(list_all5_response);

      list_all5_response.poss_words.forEach((item, i) => {
        list_all5_global.push(item);
      });
      console.log('wglobal', list_all5_global.length);
    };


    paraula_valida = false;
    list_all5_global.forEach((item, i) => {
      if(paraula == item){
        console.log(paraula, item);
        paraula_valida = true;
      };
    });

  }

  if(paraula_valida){
    var paraula_input = "PIZZA";
    var resultat_input = "CCCCC";
    
    const data = {paraula_input, resultat_input};
    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers:{'Content-Type': 'application/json'}
    };
    const response = await fetch('/getSuggerencia', options);
    const words = await response.json();
    console.log('DB received:');
    console.log(words);

    return true
  }else{
    document.getElementById("seguent"+torn).classList.remove('bg-success')
    document.getElementById("seguent"+torn).classList.add('bg-danger')
    document.getElementById("seguent"+torn).textContent = "Paraula Invàlida"
    console.log('return false', 'seguent'+torn)
    return false
  }

}
