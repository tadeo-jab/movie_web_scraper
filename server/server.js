const express = require("express")
const { spawn } = require('child_process');
const scraperPersistence = require('./persistence/scraper-persistence.json');
const qs = require('qs')

const app = express()
const movieScraperPath = 'scraper/imdb_scraper.py'
const countryScraperPath = 'scraper/country_scraper.py'


function scraperChildProcess(path, params){
    const pythonProcess = spawn('python', [path, JSON.stringify(params)]);

    let dataBuffer = '';

    pythonProcess.stdout.on('data', (data) => {
        dataBuffer += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
    });



    pythonProcess.on('close', (code) => {
        if (code === 0) {
        try {
            const scrapedData = JSON.parse(dataBuffer);
            res.status(200).json(scrapedData);
        } catch (err) {
            res.status(500).json({ error: 'Failed to parse Python script output' });
        }
        } else {
            res.status(500).json({ error: 'Python script failed to execute', data: dataBuffer });
        }
        
    });
}


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

app.get("/filters", (req, res)=>{
    const filters = scraperPersistence.filters

    const countryProcess = spawn('python', [countryScraperPath, JSON.stringify(scraperPersistence.client_utils)]);

    let countryBuffer = '';

    countryProcess.stdout.on('data', (data) => {
        countryBuffer += data.toString();
    });

    countryProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
    });



    countryProcess.on('close', (code) => {
        if (code === 0) {
        try {
            const countryData = JSON.parse(countryBuffer);
            const countryIndex =  filters.findIndex(fil => fil.filterId === "country")
            filters[countryIndex].options = countryData.data
            res.status(200).json(filters);
        } catch (err) {
            res.status(500).json({ error: 'Failed to parse Python script output' });
        }
        } else {
            res.status(500).json({ error: 'Python script failed to execute', data: countryBuffer });
        }
    });
})


app.get('/search', (req, res) => {

    //res.status(200).json({'xd':req.query})
    
    //JSON.stringify(req.query)
    
    const pythonProcess = spawn('python', [movieScraperPath, JSON.stringify(req.query), JSON.stringify(scraperPersistence)]);

    let dataBuffer = '';

    pythonProcess.stdout.on('data', (data) => {
        dataBuffer += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
    });



    pythonProcess.on('close', (code) => {
        if (code === 0) {
        try {
            const scrapedData = JSON.parse(dataBuffer);
            res.status(200).json(scrapedData);
        } catch (err) {
            res.status(500).json({ error: 'Failed to parse Python script output' });
        }
        } else {
            res.status(500).json({ error: 'Python script failed to execute', data: dataBuffer });
        }
        
    });
    
});

app.listen(5000, () => {console.log("Server started on port 5000")})