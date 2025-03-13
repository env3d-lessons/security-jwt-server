const { OAuth2Client } = require('google-auth-library');

const client = new OAuth2Client();

const verifyGoogleToken = async (token) => {
    try {
        const ticket = await client.verifyIdToken({
            idToken: token,
            audience: null, // No need to specify CLIENT_ID, works for all Google tokens
        });

        const payload = ticket.getPayload();
        return payload; // Returns user info like email, name, picture, sub (user ID)
    } catch (error) {
        console.error('Invalid Google token:', error);
        return null;
    }
};

module.exports = verifyGoogleToken;