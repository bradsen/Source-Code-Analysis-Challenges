const express = require('express');
const axios = require('axios');
const { URL } = require('url');

const app = express();

app.get('/profile', (req, res) => {
    console.log('Received request for /profile');

    // Simulated profile data
    const profileData = {
        name: 'John Doe',
        role: 'Developer'
    };
    
    res.json(profileData);
    console.log('Sent profile data response');
});

// Function to validate if URL is from an allowed domain
function isAllowedUrl(url) {
    try {
        const parsedUrl = new URL(url);
        
        // Create a URLSearchParams object with the query string of the URL
        const params = new URLSearchParams(new URL(url).search);
        
        // Check if the hostname/domain matches the whitelist
        const allowedDomains = ['www.google.com', 'www.yahoo.com']; 
        if (!allowedDomains.includes(parsedUrl.hostname)) {
            console.error('Domain not allowed:', parsedUrl.hostname);
            return false;
        }
        
        // Extract the 'id' parameter value
        const searchParams = new URLSearchParams(parsedUrl.search);
        const id = searchParams.get('id');

        // Validate the 'id' parameter value using the specified regex pattern
        //a-z: Lowercase English letters.
        //A-Z: Uppercase English letters.
        //0-9: Digits from 0 to 9
        //{1,30}:1: Minimum length of 1 character.30: Maximum length of 30 characters

        const idRegex = /^[a-zA-Z0-9]{1,30}$/; // Adjusted regex to match ASCII letters and digits

        if (!id || !idRegex.test(id)) {
            console.error('Invalid id parameter:', id);
            return false;
        }

        // If both checks pass, the URL is allowed
        return true;
        
    } catch (error) {
        console.error('Invalid URL:', error);
        return false;
    }
}

app.get('/fetch-data', async (req, res) => {
    const url = req.query.url;

    // Validate URL before making request
    if (!isAllowedUrl(url)) {
        return res.status(400).send('URL is not allowed');
    }

    console.log(`Received request for /fetch-data with URL: ${url}`);
    
    try {
        const response = await axios.get(url);
        res.send(response.data);
        console.log(`Data fetched and sent for URL: ${url}`);
    } catch (error) {
        console.error(`Error fetching data from URL: ${url}`, error);
        res.status(500).send('Error fetching data');
    }
});



app.listen(3000, () => {
    console.log('Server running on port 3000');
});
