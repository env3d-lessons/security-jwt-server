
const sqlite3 = require('sqlite3');
const sqlite = require('sqlite');
const express = require('express');
const app = express();

let validateJwt = require('./validateJwt');
const e = require('express');

const extractToken = (req) => {
    const authHeader = req.header('Authorization');  
    if (authHeader && authHeader.startsWith('Bearer ')) {
        return authHeader.split(' ')[1];  // Extract token after "Bearer "
    }
    return null;
};


// Middleware function
async function authjwt(req, res, next) {
    console.log('Extract JWT from req and check');
    const token = extractToken(req);
    const userData = await validateJwt(token);
    if (!userData) {
        return res.status(401).json({ message: 'Invalid Google token' });
    } else {
        next();
    }
};

function setupServer(db) {

    // This is a test frontend - uncomment to check it out
    // app.use(express.static('public'));
    app.use(authjwt)
    
    app.get('/info', (req, res) => {
        res.send('Full stack example');
    });

    // retrieve all unique stree names
    app.get('/streets', (req, res) => {
        db.all(`SELECT DISTINCT(name) FROM BikeRackData`)
          .then( data => {
              console.log(data);
              res.send(data);
          });
    });

    app.get('/streets/:street/', (req, res) => {
        let streetName = req.params.street;
        // query based on street
	// NOTE: this is open to SQL injection attack
        db.all(`SELECT * FROM BikeRackData WHERE name = '${streetName}'`)
          .then( data => {
              res.send(data);              
          });
        

    });

    

    let server = app.listen(8080, () => {
        console.log('Server ready', server.address().port);
    });
    
}

sqlite.open( { 
	filename: 'database.sqlite',
	driver: sqlite3.Database 
}).then( db => {
	//console.log('database opened', db);  
  setupServer(db);
  //return db.all('SELECT * from TEST');  
});

