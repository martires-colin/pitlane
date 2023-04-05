// By Colin Martires

const functions = require("firebase-functions");
const admin = require('firebase-admin');
admin.initializeApp();

exports.listUsers = functions.https.onCall((data, context) => {
    return admin.auth().listUsers().then(users => {
        return {
            listOfUsers: users
        }
    }).catch(err => {
        return err
    });
});

exports.addAdminRole = functions.https.onCall((data, context) => {
    return admin.auth().getUserByEmail(data).then(user => {
        return admin.auth().setCustomUserClaims(user.uid, {
            admin: true
        });
    }).then(() => {
        return {
            message: `${data} has been granted admin privileges`
        }
    }).catch(err => {
        return err
    });
});

exports.deleteUser = functions.https.onCall((data, context) => {
    return admin.auth().getUserByEmail(data).then(user => {
        return admin.auth().deleteUser(user.uid)
    }).then((res) => {
        return {
            message: `${data} has been deleted`,
            results: res
        }
    }).catch(err => {
        return err
    });
});