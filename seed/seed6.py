def seed(cur, fake, COUNT):
    cur.execute('SELECT id FROM Company')
    company_ids = [row[0] for row in cur.fetchall()]

    if not company_ids:
        print("Warning: No companies found. Please seed companies first.")
        return
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for company_id in company_ids:
        cur.execute(
            'INSERT INTO PostingSchedule('
            '  company_id, best_day, best_time, effectiveness_score'
            ') VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
            (
                company_id,
                fake.random_element(days_of_week),
                fake.time(pattern='%H:%M:%S'),
                fake.random.uniform(0.5, 1.0)
            )
        )
    content_types = ['text', 'image', 'video', 'story', 'reel', 'live']
    for company_id in company_ids:
        for content_type in content_types:
            cur.execute(
                'INSERT INTO ContentTypeAnalysis('
                '  company_id, content_type, engagement_rate'
                ') VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                (
                    company_id,
                    content_type,
                    fake.random.uniform(0.01, 0.2)
                )
            )
    