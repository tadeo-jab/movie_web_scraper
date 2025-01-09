const express = require("express")
const { spawn } = require('child_process');
const scraperPersistence = require('./persistence/scraper-persistence.json');

const app = express()
const movieScraperPath = 'scraper/imdb_scraper.py'
const countryScraperPath = 'scraper/country_scraper.py'

const sampleSelect = {
    genres: ['Crime', 'Thriller'],
    country: 'US',
    date: {"end": "2024-12-31", "start": "1980-01-01"},
    runtime: {"max": 180, "min": 1},
    actor: 'samuel l jackson',
    director: 'quentin tarantino',
    type: 'movie',
    rating: {"max": 9.9, "min": 5},
    parental: 'R',
    animated: false,
    popularity: {"max": 3000000, "min": 100000},
    awards: [{"eventId": 'ev0000292'}],
    company: ['co0023400']
}

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
            res.status(200).json({filters, countries:countryData});
        } catch (err) {
            res.status(500).json({ error: 'Failed to parse Python script output' });
        }
        } else {
            res.status(500).json({ error: 'Python script failed to execute', data: countryBuffer });
        }
    });
})


app.get('/search', (req, res) => {

    //JSON.stringify(req.query)
    const pythonProcess = spawn('python', [movieScraperPath, JSON.stringify(sampleSelect), JSON.stringify(scraperPersistence)]);

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