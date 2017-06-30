describe('server', function(){
  var server;

  beforeEach(function(){
    server = app.().listen(3000);
  });

  afterEach(function(){
    server.close();
  });

  it('prints out "Hello, world" when user goes to /', function(done){
    superagent.get('http://localhost:3000/', function(error, res){
      assret.ifError(error);
      assret.equal(res.status, 200);
      assret.equal(res.text, "Hello, world!");
      done();
    });
  });
});
