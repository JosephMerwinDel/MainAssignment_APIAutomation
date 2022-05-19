import random
import string
import config
from POMObjects.BaseClass import BaseApi
from Utils.Methods import APIRequest
from config import BASE_URL
import requests
from Utils.Read_Write_xlsx import XlsxReader

rd = XlsxReader()


class Tasks(BaseApi):

    def __init__(self):
        super().__init__()
        self.base_url = BASE_URL
        self.request = APIRequest()

    def add_task(self):
        self.headers = {"Authorization": "Bearer {0}".format(config.ACCESS_TOKEN)}
        payload = {
            "description": random.choice(config.TASKS_TO_DO)
        }
        response = self.request.post("{0}/task".format(self.base_url), payload, self.headers)
        return response

    def add_multiple_tasks(self, no_of_tasks=20):
        for i in range(0, no_of_tasks):
            response = self.add_task()
            rd.write_data(config.EMAIL, response)

        rd.merge_cells()

    def pagination(self, limit, skip=10):
        self.headers = {"Authorization": "Bearer {0}".format(config.ACCESS_TOKEN)}
        response = self.request.get("{0}/task?limit={1}skip={2}".format(self.base_url, limit, skip), self.headers)
        return response

    def get_all_tasks(self):
        self.headers = {"Authorization": "Bearer {0}".format(config.ACCESS_TOKEN)}
        response = self.request.get("{0}/task", self.headers)
        return response
