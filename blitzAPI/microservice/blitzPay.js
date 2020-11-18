var pbkdf2 = require('pbkdf2-sha256');

var checkPassword = function(password, algorithm, salt, iterations, original){
    var hashed = pbkdf2(password, new Buffer(salt), iterations, 32).toString('base64');
    var finalPass = algorithm +'$'+ iterations +'$'+ salt +'$'+  hashed;

    // console.log(original);
    // console.log(finalPass);

    if(original==finalPass){
        return true
    }
    return false
}

module.exports = {
    topUpAccount: function(connection, username, amount) {
        return new Promise(function(resolve, reject) {

            connection.query('UPDATE `blitz`.`blitz_pay_saldo` SET `balance`=`balance`+? WHERE `username`=?;',[amount, username], function (err, rows, fields) {
                if (err) {
                    return reject('Internal Server Error');
                }
                if(rows['changedRows']==0){
                    reject('Error occurred, username do not exists')
                }

                resolve('Successfully Top Up '+username +' with amount : '+amount)
            })
            
        })
    },
    payment: function(connection, username, password, amount) {
        return new Promise(function(resolve, reject) {

            connection.query('SELECT `password` FROM auth_user WHERE `username`=?;', [username], function (err, result) {
                if (err) {
                    return reject('Internal Server Error');
                }
                if(result.length == 0){
                    reject('Error occurred, username do not exists')
                }
                
                original = result[0]['password']

                arr_password = original.split('$')
                authentication = checkPassword(password, arr_password[0], arr_password[2], parseInt(arr_password[1]), original)

                if(authentication){
                    //cek dana cukup
                    connection.query('SELECT balance FROM `blitz_pay_saldo` WHERE `username`=?;',[username], function (err, result) {
                        if (err) {
                            return reject('Internal Server Error');
                        }

                        if(result[0]['balance'] < amount){
                            return reject('Current Balance '+result[0]['balance']+' not enough.');
                        } else{
                            connection.query('UPDATE `blitz`.`blitz_pay_saldo` SET `balance`=`balance`-? WHERE `username`=?;',[amount, username], function (err, rows, fields) {
                                if (err) {
                                    return reject('Internal Server Error');
                                }
                                resolve('Successfully Credit '+username +', amount charged : '+amount+". "+ new Date())
                            })
                        }
                    })
                }else{
                    reject('Incorrect Username and Password')
                }

            })
            
        })
        
    }
}
