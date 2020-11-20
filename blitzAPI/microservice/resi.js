
module.exports = {
    getOrderDetail: function(connection, username, password, date) {
        return new Promise(function(resolve, reject) {

            connection.query("UPDATE `blitz1`.`core_blitzpay` SET `saldo`=`saldo`+? WHERE `user_id`=(SELECT `id` FROM `auth_user` WHERE `blitz1`.`auth_user`.`username`=?);",[amount, username], function (err, rows, fields) {
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
}
