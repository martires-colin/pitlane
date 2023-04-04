// By Colin Martires

const functions = require("firebase-functions");
const admin = require('firebase-admin');
admin.initializeApp();

exports.listUsers = functions.https.onCall((data, context) => {
    //list all registered users
    return admin.auth().listUsers().then(users => {
        return {
            listOfUsers: users
        }
    }).catch(err => {
        return err
    });
});