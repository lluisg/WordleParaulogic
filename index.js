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

// PART PARAULOGIC -------------------------------------------------------------
// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------

app.post('/getWords', async (request, response) => {

    const lletra = request.body.lletra;
    const lletraM = lletra.toUpperCase()
    const lletres = request.body.lletres+lletra;
    const lletresM = lletres.toUpperCase()
    var list_words = []

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

// PART WORDLE -----------------------------------------------------------------
// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------

app.post('/getAll5', async (request, response) => {

    var poss_words = []

    db.collection("wordsCatalan5").find({}).project({_id:0, word:1}).toArray(function(err, result) {
        if (err) response.json('error');

        result.forEach(function (item, index) {
            poss_words.push(item['word'])
        });

        console.log(poss_words)
        console.log('retornem', poss_words.length, 'paraules')
        response.json({poss_words});
    });
});

app.post('/getSuggerencia', async (request, response) => {
    const paraula = request.body.paraula_input;
    const resultat = request.body.resultat_input;

    var poss_words = []
    var sugg = "aa"

    // db.collection("wordsCatalan5").find({}).project({_id:0, word:1}).toArray(function(err, result) {
    //     if (err) response.json('error');
    //
    //     result.forEach(function (item, index) {
    //         poss_words.push(item['word'])
    //     });
    //
    //     console.log(poss_words)
    //     console.log('retornem', poss_words.length, 'paraules')
    //     response.json({poss_words});
    // });
    console.log('got suggerencia', sugg)
    response.json({sugg});

});
