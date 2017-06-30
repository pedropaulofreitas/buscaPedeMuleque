var express = require('express');
var router = express.Router();

//Mongoose import
var mongoose = require('mongoose');

//Mongoose connection to MongoDB
mongoose.connect('mongodb://localhost:27017/crawledData', function(error){
  if(error){
    console.log('the error is:' + error);
  }
});

//Mongoose Schema definition
var Schema = mongoose.Schema;
var ItemSchema = new Schema({
    titulo : String,
    mercado : String,
    regiao : String,
    preco : String,
    timestamp : String,
    validade : String,
    quantidade : String,
    categoria : String,
    loja : String

});

//Mongoose Model definition
var Item = mongoose.model('items', ItemSchema);


/* GET home page. */
router.get('/', function(req, res, next) {
   res.render('index', { title: '+Barata' });

});


/* GET home page. */
router.post('/', function(req, res) {

  var keyword = req.body.keyWord;

  //executando o script que ira chamar o spark
  require('child_process').exec('~/grandesDados/play.sh ' +  keyword,
    function (error, stdout, stderr) {
      console.log('stdout: ' + stdout);
      console.log('stderr: ' + stderr);
      if (error !== null) {
        console.log('exec error: ' + error);
      }
  });

  //RegEx based on keyword tiped by the user on the search input
  // the /i/ paramenter means case insensitive
  Item.find({"titulo" : new RegExp(keyword,'i')}, function (err, docs){
    res.json(docs);
  });
});

module.exports = router;
