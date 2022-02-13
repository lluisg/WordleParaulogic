const Express = require("express");
const MongoClient = require("mongodb").MongoClient;
const ObjectId = require("mongodb").ObjectID;

var app = Express();
app.use(Express.static(__dirname + '/public'));
app.use(Express.json());

require('dotenv').config()
var favicon = require('serve-favicon');
var path = require('path');
app.use(favicon(path.join(__dirname,'public','images','logo.ico')));
var _ = require('underscore');

const CONNECTION_URL = process.env.CONNECTION_URL;
const DATABASE_NAME = "wordleDB";

// CONNECT MONGODB DATABASE
const port = process.env.PORT || 3000;
var server = app.listen(port, () => {
    console.log('listening at '+port)
    MongoClient.connect(CONNECTION_URL, { useNewUrlParser: true, useUnifiedTopology: true }, (error, client) => {
        if(error) {
            throw error;
        }
        db = client.db(DATABASE_NAME);
        console.log("Connected to `" + DATABASE_NAME + "`!");
    });
});


app.post('/getWords', async (request, response) => {


    const lletra = request.body.lletra;
    // const lletra = 'E';
    const lletraM = lletra.toUpperCase()
    const lletres = request.body.lletres+lletra;
    // const lletres = 'CMDOL';
    const lletresM = lletres.toUpperCase()
    var list_words = []
    // const poss_words = ['una', 'dua', 'trenti', 'cada', 'cadada', 'cadas'];

    // db.collection("wordsCatalan_small").find({}).project({_id:0, word:1}).toArray(function(err, result) {
    db.collection("wordsCatalan").find({}).project({_id:0, word:1}).toArray(function(err, result) {

        if (err) response.json('error');

        result.forEach(function (item, index) {
            list_words.push(item['word'])
        });
        console.log(lletraM, lletresM, list_words.length)

        var poss_words = FilterPossibleWords(lletraM, lletresM, list_words)

        console.log(poss_words)
        console.log('retornem', poss_words.length, 'paraules')
        response.json({poss_words});
    });
});

function FilterPossibleWords(lletra, lletres, paraules) {
  var words_lletra = [];
  var words_lletres = [];
  paraules.forEach(validarLletra);
  words_lletra.forEach(validarLletres);

  function validarLletra(word) {
    // mira que la paraula contingui la lletra
    if(word.includes(lletra)){
      words_lletra.push(word);
    }
  }

  function validarLletres(word) {
    // mira que totes les lletres de la paraula siguin valides
    let valid = true;
    for (var i = 0; i < word.length; i++) {
      let letter = word.charAt(i);
      if(!lletres.includes(letter)){
        valid = false;
      }
    }
    if(valid){
      words_lletres.push(word)
    }
  }

  return words_lletres.sort()
}
