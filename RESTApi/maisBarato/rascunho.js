
/*POST home page. */
router.post('/', function(req, res){

  var keyword = req.body.keyWord;

  //Conecting to mongodb
  var mongodb  = require('mongodb');
  var uri = 'mongodb://localhost:27017/crawledData';
  mongodb.MongoClient.connect(uri, function(error, db){
    if(error){
      console.log(error);
      process.exit(1);
    }

      db.items.find({ "titulo": "Chá Mate DO BEM  Limão ou  Natural TP 1 L" }).toArray(function(error, docs){
        if(error){
          console.log(error);
          process.exit(1);
        }

        console.log('Found docs:');
        docs.forEach(function(doc){
          test = JSON.stringfy(doc);
          console.log(JSON.stringfy(doc));
        });
        process.exit(0);
      });

  });
  var html = 'vc buscou: ' + test + '.<br>' +
             '<a href="/">Try again.</a>';
  res.send(html)
  });
