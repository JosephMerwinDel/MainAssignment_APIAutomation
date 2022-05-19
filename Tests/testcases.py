import pytest

import Tests.asserts
import config
from POMObjects.Tasks import Tasks
from POMObjects.UserClass import Users
from Tests.BaseTest import BaseTest
from Tests.asserts import Asserts

users = Users()
tasks = Tasks()


@pytest.mark.usefixtures("setup")
class TestFeatures(BaseTest):

    def test_user_is_created(self, config):
        log = self.getLogger()
        response = users.create_user()
        try:
            Asserts.assert_code_status(response, 201)
            Asserts.assert_response_content_type(response)
            log.info("Status code is {0}.User created successfully".format(response.status_code))
        except AssertionError as err:
            log.exception(str(err))
            raise err

        get_response = users.get_user()
        try:
            assert (response.as_dict["user"]["name"] == get_response.as_dict["name"])
            assert (response.as_dict["user"]["email"] == get_response.as_dict["email"])
            assert (response.as_dict["user"]["age"] == get_response.as_dict["age"])
            log.info(
                "Name: {0}\n Email: {1}\n".format(response.as_dict["user"]["name"], response.as_dict["user"]["email"]))
        except AssertionError as err:
            log.exception(str(err))
            raise err

    def test_duplicate_user_creation(self):
        log = self.getLogger()
        get_response = users.get_user()
        duplicate_response = users.duplicate_user(get_response.as_dict)
        try:
            Asserts.assert_code_status(duplicate_response, 400)
            log.info("Status code :" + str(duplicate_response.status_code))
        except AssertionError as err:
            log.exception(str(err))
            raise err

    def test_user_login(self):
        log = self.getLogger()
        response = users.login()
        try:
            Asserts.assert_code_status(response, 201)
            Asserts.assert_response_content_type(response)
            log.info("Status code :" + str(response.status_code))
        except AssertionError as err:
            log.exception(str(err))
            raise err

    def test_add_task(self):
        log = self.getLogger()
        response = tasks.add_task()
        try:
            Asserts.assert_code_status(response, 201)
            Asserts.assert_response_content_type(response)
        except AssertionError as err:
            log.exception(str(err))
            raise err


    def test_add_multiple_tasks(self):
        log = self.getLogger()
        tasks.add_multiple_tasks()
        response = tasks.get_all_tasks()
        try:
            assert (response.status_code == 200), "Status code is not 200. Rather found : " + str(response.status_code)
            assert (response.as_dict['count'] == 20)
            for task in response.as_dict['data']:
                assert task["completed"] == False
                assert task["description"] in config.TASKS_TO_DO
        except AssertionError as err:
            log.exception(str(err))
            raise err

    def test_validate_pagination(self):
        limits = [2, 5, 6]
        for limit in limits:
            response = tasks.pagination(limit)
            assert (response.status_code == 200, "Status code is not 200. Rather found : " + str(response.status_code))
