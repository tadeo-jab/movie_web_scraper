const express = require("express")
const { spawn } = require('child_process');
const scraperPersistence = require('./persistence/scraper-persistence.json');
const qs = require('qs')

const app = express()

const movieScraperPath = 'scraper/imdb_scraper.py'
const countryScraperPath = 'scraper/country_scraper.py'

//Runs the Python programs as Child Processes

function scraperChildProcess(path, args1={}, args2={}){
    return new Promise((res, rej) => {
        const pythonProcess = spawn('python', [path, JSON.stringify(args1), JSON.stringify(args2)]);

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                res(JSON.parse(output));
            } else {
                rej(new Error(`Process exited with code ${code}: ${errorOutput}`));
            }
        });

    });
}


//Parses non-string values from the query params

app.set('query parser', (queryString) => {
    return qs.parse(queryString, {
        decoder: (value) => {
        if (!isNaN(value)) {
            return Number(value);
        }
        if (value === 'true') {
            return true;
        }
        if (value === 'false') {
            return false;
        }
        return value;
        },
    });
});


//Passes the necessary initial data to the front-end.
//Would usually be part of some sort of database, but it's emulated through a JSON persistence file.

//Runs the "Country Scraper" process, returning a list of countries and their codes to be passed as filters for the movie search.

app.get("/filters", async (req, res)=>{
    try{
        const filters = scraperPersistence.filters
    
        const countryData = await scraperChildProcess(countryScraperPath, scraperPersistence.client_utils)
    
        const countryIndex =  filters.findIndex(fil => fil.filterId === "country")
        filters[countryIndex].options = countryData.data
    
        res.status(200).json(filters);
    }
    catch(err){
        res.status(500).json({error: err})
    }
})


//Passes the returned movie data

app.get('/search', async (req, res) => {
    try{
        const moviesData = await scraperChildProcess(movieScraperPath, req.query, scraperPersistence)
        res.status(200).json(moviesData);
    }
    catch(err){
        res.status(500).json({error: err})
    }
});

app.listen(5000, () => {console.log("Server started on port 5000")})