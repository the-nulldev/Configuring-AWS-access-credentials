# tests use the AWS SDK for Python (boto3) to run AWS commands locally
# and check if they run successfully to determine if the tasks were completed correctly
# the tests will pass if the commands run successfully and fail if they do not

from hstest import StageTest, TestedProgram, CheckResult, dynamic_test
from boto3 import Session


# the function below checks if AWS credentials are configured on the machine
# it does this by running a command locally to create a CLI session
# this will fail if the credentials are not configured locally
def check_aws_credentials():
    try:
        session = Session()
        session.get_credentials()
    except Exception:
        return False
    return True


# the function below checks if AWS credentials are correct (i.e. if they can be used to make a call to AWS STS)
# it does this by running a command to create a session for the profile "Hyperprofile" and a client for the STS service
# finally, it runs the AWS "get_caller_identity" command which will fail if the credentials are not correct
# the function returns True if the command runs successfully and False if it fails
def check_aws_credentials_correct():
    try:
        session = Session(profile_name="Hyperprofile")
        sts = session.client('sts')
        sts.get_caller_identity()
    except Exception:
        return False
    return True


class TestTask(StageTest):
    # these tests check if the AWS SDK commands executed above ran successfully
    # if they ran successfully, it means that the specified tasks were completed and the tests will pass
    # if they did not run successfully, it means you have not completed the tasks correctly and the tests will fail

    @dynamic_test
    def test_aws_credentials_configured(self):
        if not check_aws_credentials():
            return CheckResult.wrong('AWS credentials are not configured.')
        return CheckResult.correct()

    @dynamic_test
    def test_aws_credentials_correct(self):
        if not check_aws_credentials_correct():
            return CheckResult.wrong('The configured credentials are not correct.')
        return CheckResult.correct()


if __name__ == '__main__':
    TestTask().run_tests()
