INSERT INTO django_banking_trade (date, net, vat, country_id, currency_id, trade_type_id)
SELECT TO_DATE(temp.date, 'YYYY/MM/DD')                                         AS date,
       ROUND((temp.net::float / django_banking_currencyvalue.rate)::numeric, 2) AS net,
       ROUND((temp.vat::float / django_banking_currencyvalue.rate)::numeric, 2) AS vat,
       django_banking_country.id                                                AS country_id,
       django_banking_currency.id                                               AS currency_id,
       django_banking_tradetype.id                                              AS trade_type_id
FROM temp_trades_import AS temp
         JOIN django_banking_currency ON django_banking_currency.iso_code = temp.currency
         JOIN django_banking_currencyvalue
              ON django_banking_currency.id = django_banking_currencyvalue.currency_id AND
                 django_banking_currencyvalue.day = DATE_TRUNC('day', TO_DATE(temp.date, 'YYYY/MM/DD'))
         JOIN django_banking_country ON temp.country ILIKE django_banking_country.slug OR
                                        temp.country ILIKE ('%' || django_banking_country.label || '%')
         JOIN django_banking_tradetypespelling ON temp.trade_type ILIKE django_banking_tradetypespelling.spelling
         JOIN django_banking_tradetype
              ON django_banking_tradetype.id = django_banking_tradetypespelling.trade_type_id
WHERE temp.date ~ '^\d{4}\/\d{1,2}\/\d{1,2}$';
