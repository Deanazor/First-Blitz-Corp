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
    getOrderDetail: function(connection, username, password, date) {
        return new Promise(function(resolve, reject) {

            connection.query('SELECT `id`,`password` FROM auth_user WHERE `username`=?;', [username], function (err, result) {
                if (err) {
                    return reject('Internal Server Error 0');
                }
                if(result.length == 0){
                    return reject('Error occurred, username does not exists')
                }
                
                original = result[0]['password']

                arr_password = original.split('$')
                authentication = checkPassword(password, arr_password[0], arr_password[2], parseInt(arr_password[1]), original)

                transport_id = result[0]['id']
                if(authentication){
                    connection.query('SELECT seller_address.username AS nama_pengirim, seller_address.street_address AS alamat_pengirim, seller_address.apartment_address AS alamat_bangunan_pengirim, seller_address.country AS negara_pengirim, seller_address.zip AS zip_pengirim, buyer_address.username AS nama_penerima, buyer_address.street_address AS alamat_penerima, buyer_address.apartment_address AS alamat_bangunan_penerima, buyer_address.country AS negara_penerima, buyer_address.zip AS zip_penerima FROM ( SELECT auth_user.username, core_address.id, core_address.street_address, core_address.apartment_address, core_address.country, core_address.zip FROM core_order INNER JOIN core_address ON core_order.shipping_provider_id = core_address.id INNER JOIN core_seller ON core_order.seller_id = core_seller.id INNER JOIN auth_user ON core_seller.user_id = auth_user.id INNER JOIN core_transport ON core_order.shipping_provider_id = core_transport.id WHERE DATE(core_order.ordered_date) = ? AND core_transport.user_id = ? ) AS seller_address INNER JOIN ( SELECT auth_user.username, core_address.id, core_address.street_address, core_address.apartment_address, core_address.country, core_address.zip FROM core_order INNER JOIN core_address ON core_order.shipping_address_id = core_address.id INNER JOIN auth_user ON core_order.user_id = auth_user.id INNER JOIN core_transport ON core_order.shipping_provider_id = core_transport.id WHERE DATE(core_order.ordered_date) = ? AND core_transport.user_id = ? ) AS buyer_address ON seller_address.id = buyer_address.id ; ',[date, transport_id, date, transport_id],
                        function (err, result) {
                            console.log(result)
                            if (err) {
                                console.log(err)
                                return reject('Internal Server Error 1');
                            }

                            return resolve(result)

                        })
                }
            })
        })
    },
    updateStatus: function(connection, username, password, order_id, status) {
        return new Promise(function(resolve, reject) {

            connection.query('SELECT `id`,`password` FROM auth_user WHERE `username`=?;', [username], function (err, result) {
                if (err) {
                    return reject('Internal Server Error 0');
                }
                if(result.length == 0){
                    return reject('Error occurred, username does not exists')
                }
                
                original = result[0]['password']

                arr_password = original.split('$')
                authentication = checkPassword(password, arr_password[0], arr_password[2], parseInt(arr_password[1]), original)

                transport_id = result[0]['id']
                if(authentication){
                    connection.query('SELECT seller_address.username AS nama_pengirim, seller_address.street_address AS alamat_pengirim, seller_address.apartment_address AS alamat_bangunan_pengirim, seller_address.country AS negara_pengirim, seller_address.zip AS zip_pengirim, buyer_address.username AS nama_penerima, buyer_address.street_address AS alamat_penerima, buyer_address.apartment_address AS alamat_bangunan_penerima, buyer_address.country AS negara_penerima, buyer_address.zip AS zip_penerima FROM ( SELECT auth_user.username, core_address.id, core_address.street_address, core_address.apartment_address, core_address.country, core_address.zip FROM core_order INNER JOIN core_address ON core_order.shipping_provider_id = core_address.id INNER JOIN core_seller ON core_order.seller_id = core_seller.id INNER JOIN auth_user ON core_seller.user_id = auth_user.id INNER JOIN core_transport ON core_order.shipping_provider_id = core_transport.id WHERE DATE(core_order.ordered_date) = ? AND core_transport.user_id = ? ) AS seller_address INNER JOIN ( SELECT auth_user.username, core_address.id, core_address.street_address, core_address.apartment_address, core_address.country, core_address.zip FROM core_order INNER JOIN core_address ON core_order.shipping_address_id = core_address.id INNER JOIN auth_user ON core_order.user_id = auth_user.id INNER JOIN core_transport ON core_order.shipping_provider_id = core_transport.id WHERE DATE(core_order.ordered_date) = ? AND core_transport.user_id = ? ) AS buyer_address ON seller_address.id = buyer_address.id ; ',[date, transport_id, date, transport_id],
                        function (err, result) {
                            console.log(result)
                            if (err) {
                                console.log(err)
                                return reject('Internal Server Error 1');
                            }

                            return resolve(result)

                        })
                }
            })
        })
    }

}
