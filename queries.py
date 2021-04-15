def get_country_id(country):
    return f'WITH s as (SELECT id, "name" FROM countries WHERE "name" = \'{country}\'), ' \
           f'i as (INSERT INTO countries ("name") SELECT \'{country}\' WHERE NOT EXISTS (SELECT 1 FROM s)' \
           f'RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s'