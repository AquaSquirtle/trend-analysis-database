def seed(cur, fake, COUNT):
    for _ in range(COUNT):
        cur.execute(
            'INSERT INTO Users (name, email, phone, password_hash, created_at) '
            'VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
            (
                fake.name(),
                fake.unique.email(),
                fake.phone_number(),
                fake.password(),
                fake.date_time_this_year()
            )
        )

    social_networks = ['Facebook', 'Twitter', 'Instagram', 'LinkedIn', 'TikTok']
    for network in social_networks:
        cur.execute(
            'INSERT INTO SocialNetwork (name) VALUES (%s) ON CONFLICT DO NOTHING',
            (network,)
        )
