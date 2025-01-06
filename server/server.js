const express = require("express")
const { spawn } = require('child_process');
const scraperPersistence = require('./persistence/scraper-persistence.json');

const app = express()
const scraperPath = 'scraper/imdb_scraper.py'

const sampleSelect = {
    genres: ['Crime', 'Thriller'],
    country: 'US',
    date: {"end": "2024-12-31", "start": "1980-01-01"},
    runtime: {"max": 180, "min": 1},
    actor: 'nm0000233',
    director: 'nm0000168',
    type: 'movie',
    rating: {"max": 9.9, "min": 5},
    parental: 'R'
}

app.get("/filters", (req, res)=>{
    res.status(200).json(scraperPersistence)
})


app.get('/search', (req, res) => {

    //JSON.stringify(req.query)
    const pythonProcess = spawn('python', [scraperPath, JSON.stringify(sampleSelect), JSON.stringify(scraperPersistence)]);

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