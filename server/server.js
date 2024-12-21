const express = require("express")
const { spawn } = require('child_process');


const app = express()

const constants = {
    filters:{
        year: ["1890", "1980", "1990", "2000", "2010"],
        genre: ["action", "adventure", "animation", "comedy","crime","documentary","drama","family","fantasy","history","horror","music","mystery","romance","science-fiction","thriller","tv-movie","war","western"]
    },
    url: "https://letterboxd.com/films/popular/",
    pagelimit: 72
}

app.get("/api", (req, res) => {
    res.json("xd")
})

app.get('/search', (req, res) => {
    const pythonProcess = spawn('python', ['scraper/letterboxd_scraper.py', JSON.stringify(req.query), JSON.stringify(constants)]);

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
            const parsedData = JSON.parse(dataBuffer);
            res.status(200).json(parsedData);
        } catch (err) {
            res.status(500).json({ error: 'Failed to parse Python script output' });
        }
        } else {
            res.status(500).json({ error: 'Python script failed to execute', data: dataBuffer });
        }
    });
});

app.listen(5000, () => {console.log("Server started on port 5000")})