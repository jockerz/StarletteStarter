from apps.utils.string import gen_random, gen_id, gen_apikey, mask_email


class TestUtilsString:
    def test_gen_random(self):
        assert len(gen_random()) == 32
        assert len(gen_random(1)) == 1
        assert gen_random(10, 'A') == 'A' * 10

    def test_gen_id(self):
        new_id = gen_id(10)
        assert len(new_id) != 10

    def test_gen_apikey(self):
        new_apikey = gen_apikey()
        assert len(new_apikey.split('.')) == 2

    def test_mask_mail(self):
        email = 'mail@any.host'
        masked = mask_email(email)
        assert masked != email
        assert '*' in masked

        parts = masked.split('@')
        assert parts[0] != 'mail'
        assert '*' in parts[0]
        assert parts[1] != 'any.host'
        assert '*' in parts[1]
