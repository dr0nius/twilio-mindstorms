/**
 *  Sync Token Generator
 *
 *  This snippet shows you how to mint Access Tokens for Twilio Sync. Please note, this is for prototyping purposes
 *  only. You will want to validate the identity of clients requesting Access Token in most production applications and set
 *  the identity field correspondingly when minting the Token.
 *
 *  Pre-requisites
 *    - Create an API Key (https://www.twilio.com/console/sync/tools)
 */

exports.handler = function(context, event, callback) {
  // make sure you enable ACCOUNT_SID and AUTH_TOKEN in Functions/Configuration
  const ACCOUNT_SID = context.ACCOUNT_SID;

  const SERVICE_SID = 'default';
  const API_KEY = context.TWILIO_API_KEY;
  const API_SECRET = context.TWILIO_API_SECRET;

  // REMINDER: This identity is only for prototyping purposes
  const IDENTITY = 'DroidController';

  const AccessToken = Twilio.jwt.AccessToken;
  const SyncGrant = AccessToken.SyncGrant;

  const syncGrant = new SyncGrant({
    serviceSid: SERVICE_SID
  });

  const accessToken = new AccessToken(
    ACCOUNT_SID,
    API_KEY,
    API_SECRET
  );

  accessToken.addGrant(syncGrant);
  accessToken.identity = IDENTITY;

  callback(null, {
    token: accessToken.toJwt(),
    identity: IDENTITY
  });
}
