var casper = require('casper').create()
var links
// Define variables
// var HTTP_DOMAIN ='http://casperjs.org/'
var HTTP_DOMAIN = 'https://conet.caixaontinyent.es/BEWeb/2045/6045/inicio_identificacion.action'
var USER = 'XXXXXXX'
var PASSWD = '0000'
var loginButton = 'botonEntrar'
var fs = require('fs');

// Opens caixaontinyent homepage
casper.start(HTTP_DOMAIN)

casper.then(function () {
  // Fill login form
  this.fill('form[name="login"]', {
    'PAN': '',
    'AUXPIN': ''
  })
  // this.capture('test-screen1.png')
  // Click to login
  this.click('input#botonEntrar')
}).wait(2000)
.then(function () {
  // this.capture('1afterLogin.png')
  // Click on right corner
  this.click('input#botonEntrarConex')
}).wait(2000)
.then(function () {
  // this.capture('2afterLogin.png')
  // Get the corresponding frame
  this.page.switchToFrame('fcontenido')
  // var page = this.getHTML()
  // fs.write("page.html", page, "wb")
  // Set last movements checked
  // this.click('input#ultimovs')
  this.fill('form[name="datos"]', {'ultimovs': 'checked'})
  // this.capture('3checkedLastMovs.png')
  this.click('button#enviar')
}).wait(2000)
.then(function () {
  // this.capture('4showMovs.png')
  this.page.switchToFrame('fcontenido')
  var page = this.getHTML()
  fs.write("movs.html", page, "wb")
})

casper.run(function () {
   casper.done(function () {
    this.exit()
  })
})
