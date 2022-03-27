SELECT
    CustomerId
FROM
    {{ chinook_db }}.customers
WHERE
    Country = '{{ analysis_country }}'
