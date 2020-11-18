
module.exports = {
    connectResi: function(connection) {
        return new Promise(function(resolve, reject) {
            connection.query('SELECT * FROM `blitz`.`auth_user` LIMIT 1000', function (err, rows, fields) {
                if (err) {
                    return reject(500);
                }
                resolve(rows[0])
            })
            
        })
        
    }
}
