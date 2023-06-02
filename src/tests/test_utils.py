import os, sys, json

import tools_for_testing as tft

sys.path.append("../")

import utils

class TestApplyMetadata:
    @classmethod
    def setup_class(cls):
        cls.img_path = tft.import_file("TEST_JPG.jpg", "TestApplyMetadata")
        cls.json_path = tft.import_file("TEST_JPG.jpg.json", "TestApplyMetadata")

        with open(cls.json_path) as f:
            cls.json = json.load(f)
        assert os.path.getctime(cls.img_path) != float(cls.json["creationTime"]["timestamp"])
        assert os.path.getmtime(cls.img_path) != float(cls.json["photoTakenTime"]["timestamp"])

    @classmethod
    def test_apply_metadata(cls):
        utils.apply_metadata(cls.img_path, cls.json_path)
        assert os.path.getctime(cls.img_path) == float(cls.json["creationTime"]["timestamp"])
        assert os.path.getmtime(cls.img_path) == float(cls.json["photoTakenTime"]["timestamp"])

    @classmethod
    def teardown_class(cls):
        for fname in [cls.img_path, cls.json_path]:
            if os.path.exists(fname):
                os.remove(fname)


class TestGroupFilesByName:
    def test_edited_image_groups_up_with_regular(self):
        files = ["COOLNAME.jpg", "COOLNAME-edited.jpg"]
        result = utils.group_files_by_name(files)
        assert result["COOLNAME"]["images"] == set(files)

    def test_images_with_different_name_do_not_group_up(self):
        files = ["COOLNAME.jpg", "OTHERNAME.jpg"]
        result = utils.group_files_by_name(files)
        assert result["COOLNAME"]["images"] == set([files[0]])
        assert result["OTHERNAME"]["images"] == set([files[1]])

    def test_image_groups_with_json(self):
        files = ["COOLNAME.jpg", "COOLNAME.jpg.json", "OTHERNAME.jpg"]
        result = utils.group_files_by_name(files)
        assert result["COOLNAME"] == {
            "images": {"COOLNAME.jpg"},
            "json": "COOLNAME.jpg.json"
        }

