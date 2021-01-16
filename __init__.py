from ovos_utils.waiting_for_mycroft.base_skill import killable_intent, MycroftSkill
from mycroft import intent_file_handler
from time import sleep


class Test(MycroftSkill):
    """
    send "mycroft.skills.abort_question" and confirm only get_response is aborted
    send "mycroft.skills.abort_execution" and confirm the full intent is aborted, except intent3
    send "my.own.abort.msg" and confirm intent3 is aborted
    say "stop" and confirm all intents are aborted
    """
    def __init__(self):
        self.my_special_var = "default"

    def handle_intent_aborted(self):
        self.speak("I am dead")
        # handle any cleanup the skill might need, since intent was killed
        # at an arbitrary place of code execution some variables etc. might
        # end up in unexpected states
        self.my_special_var = "default"

    @killable_intent(callback=handle_intent_aborted)
    @intent_file_handler("test.intent")
    def handle_test_abort_intent(self, message):
        self.my_special_var = "changed"
        while True:
            sleep(1)
            self.speak("still here")

    @intent_file_handler("test2.intent")
    @killable_intent(callback=handle_intent_aborted)
    def handle_test_get_response_intent(self, message):
        self.my_special_var = "CHANGED"
        ans = self.get_response("question", num_retries=99999)
        self.log.debug("get_response returned: " + str(ans))
        if ans is None:
            self.speak("question aborted")

    @killable_intent(msg="my.own.abort.msg", callback=handle_intent_aborted)
    @intent_file_handler("test3.intent")
    def handle_test_msg_intent(self, message):
        if self.my_special_var != "default":
            self.speak("someone forgot to cleanup")
        while True:
            sleep(1)
            self.speak("you can't abort me")


def create_skill():
    return Test()
