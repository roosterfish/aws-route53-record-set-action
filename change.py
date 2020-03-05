import os
import sys
import json
import boto3

from distutils import util


class AWSRoute53RecordSet:
    """
    Primary class for the handling of AWS Route 53 Record Sets.
    """
    def __init__(self):
        """
        The default constructor.
        """
        self.client = None
        self.waiter = None
        self.rr_skeleton = dict()

    def _get_env(self, variable, exit=True):
        """
        Try to fetch a variable from the environment.
        Per default the method will raise an exception if the variable isn't present.
        This behaviour can be switched off via the exit flag.
        """
        value = os.environ.get(variable)
        if not value and exit:
            raise NameError("Cannot find environment variable: " + str(variable))
        return value

    def _connect(self):
        """
        Creates a new client object which wraps the connection to AWS.
        """
        if not self.client:
            self.client = boto3.client(
                "route53",
                aws_access_key_id=self._get_env("INPUT_AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=self._get_env("INPUT_AWS_SECRET_ACCESS_KEY")
            )
            self.waiter = self.client.get_waiter("resource_record_sets_changed")

    def _set_comment(self):
        """
        Appends an additional comment field to the record set.
        """
        comment = self._get_env("INPUT_AWS_ROUTE53_RR_COMMENT", False)
        if comment:
            self.rr_skeleton["Comment"] = comment

    def _set_base_changes(self):
        """
        Creates the base skeleton required for creating a new record set.
        """
        self.rr_skeleton["Changes"] = [{
            "Action": self._get_env("INPUT_AWS_ROUTE53_RR_ACTION"),
            "ResourceRecordSet": {
                "Name": self._get_env("INPUT_AWS_ROUTE53_RR_NAME"),
                "Type": self._get_env("INPUT_AWS_ROUTE53_RR_TYPE"),
                "TTL": int(self._get_env("INPUT_AWS_ROUTE53_RR_TTL")),
                "ResourceRecords": [{
                    "Value": self._get_env("INPUT_AWS_ROUTE53_RR_VALUE")
                }]
            }
        }]

    def _build_record_set(self):
        """
        Builds up the skeleton used for modulating the record set.
        """
        self._set_comment()
        self._set_base_changes()
        return self.rr_skeleton

    def _change_record_set(self, record_set):
        """
        Requests the required change at AWS.
        """
        return self.client.change_resource_record_sets(
            HostedZoneId=self._get_env("INPUT_AWS_ROUTE53_HOSTED_ZONE_ID"),
            ChangeBatch=record_set
        )

    def _wait(self, request_id):
        """
        Waits until the requested operations is finished.
        """
        wait = self._get_env("INPUT_AWS_ROUTE53_WAIT", False)
        if wait and util.strtobool(wait):
            self.waiter.wait(
                Id=request_id,
                WaiterConfig={
                    "Delay": 10,
                    "MaxAttempts": 50
                }
            )

    def _obtain_request_id(self, result):
        """
        Grabs and returns the id of the given request.
        """
        return result["ChangeInfo"]["Id"]

    def _obtain_marshalled_result(self, result):
        """
        Grabs and returns the HTTP response of the given request.
        """
        return json.dumps(result["ResponseMetadata"], indent=4)

    def change(self):
        """
        Entrypoint for the management of a record set.
        """
        self._connect()
        record_set = self._build_record_set()
        result = self._change_record_set(record_set)
        self._wait(
            self._obtain_request_id(result)
        )
        sys.stdout.write(
            self._obtain_marshalled_result(result) + "\n"
        )


try:
    o = AWSRoute53RecordSet()
    o.change()
except Exception as e:
    sys.stderr.write(str(e) + "\n")
    sys.exit(1)
