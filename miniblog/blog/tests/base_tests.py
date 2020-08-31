def test_model_fields_label(self, model, field_label, expected_label_name):
    """A function to test the labels of each field in a model"""
    post = model.objects.get(id=1)
    field = post._meta.get_field(field_label).verbose_name
    self.assertEquals(field, expected_label_name)


def test_model_fields_max_length(self, model, field_label, expected_max_length):
    """A function to test the max lenghts of each field in a model"""
    post = model.objects.get(id=1)
    length = post._meta.get_field(field_label).max_length
    self.assertEquals(length, expected_max_length)