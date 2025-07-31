def seed(cur, fake, COUNT):
    cur.execute('SELECT id FROM Users')
    user_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT id FROM SocialNetwork')
    social_ids = [row[0] for row in cur.fetchall()]
    
    if not user_ids or not social_ids:
        return
    company_ids = []
    business_types = ['LLC', 'Corporation', 'Sole Proprietorship', 'Partnership', 'Non-profit']
    categories = ['Technology', 'Retail', 'Food & Beverage', 'Healthcare', 'Finance', 'Education', 'Manufacturing']
    
    for _ in range(COUNT):
        cur.execute(
            'INSERT INTO Company('
            '  user_id, category, business_type, name, description, location, created_at'
            ') VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id',
            (
                fake.random_element(user_ids),
                fake.random_element(categories),
                fake.random_element(business_types),
                fake.company(),
                fake.text(max_nb_chars=200),
                fake.city(),
                fake.date_time_this_year()
            )
        )
        company_id = cur.fetchone()[0]
        company_ids.append(company_id)
    for company_id in company_ids:
        for _ in range(fake.random_int(1, 3)):
            social_id = fake.random_element(social_ids)
            cur.execute(
                'INSERT INTO CompanySocialLink('
                '  company_id, social_id, url'
                ') VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                (
                    company_id,
                    social_id,
                    fake.url() + f'/{fake.user_name()}'
                )
            )
            