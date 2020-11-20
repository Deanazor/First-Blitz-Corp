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
  res.send("Ok")
})

// Handle Delivery for Transport Company
app.get('/transport/getdelivery', (req, res) => {
  console.log(req.query.date);
  res.send('ok')
  
})

app.post('/resi', (req, res) =>{

})


// Handle BlitzPay
app.post('/blitzpay/topup', (req, res) =>{
  blitzPay.topUpAccount(db, req.body['username'], req.body['amount']).then((result) =>{
    res.send(result)
  }, (result) =>{
    res.status(500)
    res.send(result)
  })
})

app.post('/blitzpay/payment', (req, res) =>{
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