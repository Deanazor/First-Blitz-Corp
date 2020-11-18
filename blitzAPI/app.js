const express = require('express');
var bodyParser = require('body-parser'); 
const app = express()
const port = 3000

// untuk parse json data
app.use(bodyParser.json());

// connect to database
var db = require('./db');

// resi library
var resi = require('./microservice/resi.js');
var blitzPay = require('./microservice/blitzPay.js');

//hash
//WW8dGnoWFTsm/63X7fiOhRk2pyfCz9wYppdpWLHCOo0=
app.get('/', (req, res) => {
  
})

app.get('/resi', (req, res) => {
  resi.connectResi(db).then((result) =>{
    res.send(result)
  }, (result) =>{
    res.status(result)
    res.send("Internal Error")
  })
  
})

app.post('/resi', (req, res) =>{

})

app.post('/topup', (req, res) =>{
  blitzPay.topUpAccount(db, req.body['username'], req.body['amount']).then((result) =>{
    res.send(result)
  }, (result) =>{
    res.status(500)
    res.send(result)
  })
})

app.post('/payment', (req, res) =>{
  blitzPay.payment(db, req.body['username'], req.body['password'], req.body['amount']).then((result) =>{
    res.send(result)
  }, (result) =>{
    res.status(500)
    res.send(result)
  })
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})