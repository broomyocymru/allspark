import datetime
import json

import requests
from allspark.core import util, logger, config


class allsparkAnalytics(object):
    def __init__(self, **kwargs):
        self.data = {
            'timestamp': ("%s" % datetime.datetime.now()),
            'allspark_version': util.allspark_version(),
            'user': util.get_user_name(),
            'host': util.get_host()
        }
        self.kwargs = kwargs

    def get_analytics(self):
        return self.data

    def add_metric(self, key, value):
        self.data[key] = value

    def get_metric(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def add_deployment_metric(self, artifact_type, file_path, result_code):
        if "deploy" not in self.data:
            self.data["deploy"] = []

        self.data["deploy"].append({
            "type": artifact_type,
            "file": file_path,
            "result": result_code,
            "timestamp": ("%s" % datetime.datetime.now())
        })

    def submit(self, data=None):
        pass


class MockAnalytics(allsparkAnalytics):
    def __init__(self, **kwargs):
        allsparkAnalytics.__init__(self)

    def submit(self, data=None):
        pass


class Splunk(allsparkAnalytics):
    def __init__(self, **kwargs):
        allsparkAnalytics.__init__(self)
        self.url = kwargs.get("url", "")
        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password", "")

    def submit(self, data=None):
        if config.get("analytics.enabled") == "Y":
            mask_values = logger.get_masks()

            if data is None:
                data_string = json.dumps(self.data, sort_keys=False) + '\n'
            else:
                data_string = json.dumps(data, sort_keys=False) + '\n'

            if mask_values is not None:
                for to_mask in mask_values:
                    data_string = data_string.replace(to_mask, "*****")

            requests.packages.urllib3.disable_warnings()
            with requests.Session() as s:
                s.post(self.url, data=data_string, auth=(self.username, self.password), verify=False)

            logger.vlog("Analytics Sent to Splunk")
            if data is None:
                logger.vjson(self.data)
            else:
                logger.vjson(data)
            return True
        else:
            logger.vlog("Analytics Disabled")
            return True
