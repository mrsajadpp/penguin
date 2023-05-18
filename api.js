const express = require('express');
const puppeteer = require('puppeteer');
const Spotify = require('spotifydl-core').default;
const SpotifyWebApi = require('spotify-web-api-node');
const bodyParser = require('body-parser');
const sanitizeFilename = require('sanitize-filename');

const launch = puppeteer.launch({ headless: true });

const app = express();
const port = 3000; // Set your desired port number

const credentials = {
    clientId: 'ae048057336e4a1b9df086e9bd17112d',
    clientSecret: 'ec448ae380df4737a6abcd3efc4c223d',
};

// Create a new instance of the SpotifyWebApi
const spotifyApi = new SpotifyWebApi({
    clientId: credentials.clientId,
    clientSecret: credentials.clientSecret,
});

const spotify = new Spotify(credentials);

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));

// parse application/json
app.use(bodyParser.json());

app.post('/download', async (req, res) => {
    try {
        const { track_url } = req.body;
        if (!track_url) {
            return res.status(400).send('Track URL is required.');
        }

        const extractSongId = (url) => (match = url.match(/^https?:\/\/(?:www\.)?open.spotify\.com\/track\/([a-zA-Z0-9]+).*$/)) ? match[1] : null;
        const songId = await extractSongId(track_url);

        spotifyApi.clientCredentialsGrant().then(
            async function (data) {
                // Save the access token to use it in subsequent requests
                spotifyApi.setAccessToken(data.body['access_token']);

                // Call the function to get song details
                getSongDetails(songId, async (songName) => {
                    const sanitizedSongName = sanitizeFilename(songName); // Sanitize the song name
                    const song = await spotify.downloadTrack(track_url, __dirname + '/src/' + sanitizedSongName + '.mp3');
                    const track = await spotify.getTrack(track_url);
                    res.json({ "song": song, "name": songName });
                });
            },
            function (err) {
                console.error(err);
                res.status(500).send('An error occurred during song download.');
            }
        );
    } catch (error) {
        console.error(error);
        res.status(500).send('An error occurred during song download.');
    }
});

function getSongDetails(songId, callback) {
    spotifyApi.getTrack(songId).then(
        function (data) {
            const song = data.body;
            callback(song.name);
        },
        function (err) {
            console.log('Something went wrong when retrieving the song details', err);
        }
    );
}

app.post('/ig/download', async (req, res) => {
    try {
        const { reel_url } = req.body;
        if (reel_url) {
            console.log(reel_url);
            const browser = await puppeteer.launch({ headless: true });
            const page = await browser.newPage();
            const newPage = await page.goto(reel_url);
            const pageTitle = await page.title();
            setTimeout(async () => {
                const video = await page.evaluate(async () => {
                    return await document.querySelector('video').src;
                });
                setTimeout( async () => {
                    console.log(video);
                    await browser.close();
                    res.json({ 'video_url': video, 'name': pageTitle, 'status': 200 });
                }, 1000);
            }, 4000); 
        } else {
            res.json({ 'error': 'Reel url is required', 'status': 404 })
        }
    } catch (error) {
        console.error(error)
        res.json({ 'error': error, 'status': 500 })
    }
})

app.listen(port, () => {
    console.log(`Express API is running on port ${port}`);
});
