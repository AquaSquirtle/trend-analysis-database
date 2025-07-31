def seed(cur, fake, COUNT):
    cur.execute('SELECT id FROM Company')
    company_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT id FROM SocialNetwork')
    social_ids = [row[0] for row in cur.fetchall()]
    
    if not company_ids or not social_ids:
        print("Warning: No companies or social networks found. Please seed those first.")
        return
    post_ids = []
    content_types = ['text', 'image', 'video']
    age_groups = ['13-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    regions = ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Oceania']
    
    for _ in range(COUNT):
        content_type = fake.random_element(content_types)
        
        cur.execute(
            'INSERT INTO ContentPost('
            '  company_id, social_id, external_id, content_type, '
            '  text_content, publish_date, url'
            ') VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id',
            (
                fake.random_element(company_ids),
                fake.random_element(social_ids),
                fake.uuid4(),
                content_type,
                fake.text(max_nb_chars=500) if content_type == 'text' else None,
                fake.date_time_this_year(),
                fake.url()
            )
        )
        post_id = cur.fetchone()[0]
        post_ids.append(post_id)
        cur.execute(
            'INSERT INTO PostMetric('
            '  post_id, likes, comments, shares, views, updated_at'
            ') VALUES (%s, %s, %s, %s, %s, %s)',
            (
                post_id,
                fake.random_int(0, 10000),
                fake.random_int(0, 1000),
                fake.random_int(0, 5000),
                fake.random_int(0, 100000),
                fake.date_time_this_month()
            )
        )
        for age_group in age_groups:
            cur.execute(
                'INSERT INTO PostDemographics('
                '  post_id, age_group, value'
                ') VALUES (%s, %s, %s)',
                (
                    post_id,
                    age_group,
                    fake.random.uniform(0, 0.5)
                )
            )
        for gender in ['male', 'female', 'other']:
            cur.execute(
                'INSERT INTO PostGender('
                '  post_id, gender, value'
                ') VALUES (%s, %s, %s)',
                (
                    post_id,
                    gender,
                    fake.random.uniform(0, 0.5)
                )
            )
        for region in regions:
            cur.execute(
                'INSERT INTO PostGeo('
                '  post_id, region, value'
                ') VALUES (%s, %s, %s)',
                (
                    post_id,
                    region,
                    fake.random.uniform(0, 0.5)
                )
            )
            