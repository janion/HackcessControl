import re
from word2number.w2n import word_to_num
from threading import Thread
from time import time, sleep

from smart_home.client_implementations.voice_assistant.commands.Command import Command


class TimerThread(Thread):

    def __init__(self, time_to_wait, on_complete_callback):
        super().__init__(target=self._await_alarm, args=[time_to_wait], daemon=True)
        self.on_complete_callback = on_complete_callback
        self.start_time = time()
        self.stopped = False
        self.start()

    def stop(self):
        self.stopped = True

    def _await_alarm(self, time_to_wait):
        while time() < self.start_time + time_to_wait:
            sleep(1)
            if self.stopped:
                return
        # Beep
        print("Beep")
        self.on_complete_callback(self)


class TimerCommand:

    def __init__(self, regex, action_group, hours_group, and_group_1, minutes_group, and_group_2, seconds_group):
        self.regex = regex
        self.action_group = action_group
        self.hours_group = hours_group
        self.and_group_1 = and_group_1
        self.minutes_group = minutes_group
        self.and_group_2 = and_group_2
        self.seconds_group = seconds_group


class TimerCommand(Command):

    START_TIMER_FOR_X_REGEX = TimerCommand(".*(start|set)(?: a?)? timer for ((.*?) hour[s]?)?((?: and?)?)[ ]?((.*?)[ -]minute[s]?)?((?: and?)?)[ ]?((.*?) second[s]?)?.*?",
                                           1, 3, 4, 6, 7, 9)
    START_X_TIMER_REGEX = TimerCommand(".*(start|set)(?: a?)? ((.*?) hour[s]?)?((?: and?)?)[ ]?((.*?)[ -]minute[s]?)?((?: and?)?)[ ]?((.*?) second[s]?)? timer.*?",
                                       1, 3, 4, 6, 7, 9)
    START_TIMER_COMMAND_REGEXES = [START_TIMER_FOR_X_REGEX,
                                   START_X_TIMER_REGEX]

    CANCEL_TIMER_REGEX = ".*cancel latest timer.*?"
    CANCEL_ALL_TIMERS_REGEX = ".*cancel all timers.*?"
    CANCEL_TIMER_REGEXES = [CANCEL_TIMER_REGEX,
                            CANCEL_ALL_TIMERS_REGEX]

    def __init__(self, *args):
        super().__init__(*args)
        self.timerThreads = []

    def consume(self, parsed_speech):
        for command in self.START_TIMER_COMMAND_REGEXES:
            match = re.match(command.regex, parsed_speech.replace(" please", "").replace("please ", ""))
            if match:
                self._start_timer(match, command)
                return True

        match = re.match(self.CANCEL_TIMER_REGEX, parsed_speech.replace(" please", "").replace("please ", ""))
        if match:
            if self._stop_timer():
                self.speak_callback("OK", "cancelling latest timer")
            else:
                self.speak_callback("no timers to cancel")
            return True

        match = re.match(self.CANCEL_ALL_TIMERS_REGEX, parsed_speech.replace(" please", "").replace("please ", ""))
        if match:
            if self._stop_all_timers():
                self.speak_callback("OK", "cancelling all timers")
            else:
                self.speak_callback("no timers to cancel")
            return True

        return False

    def _stop_timer(self):
        if len(self.timerThreads) > 0:
            self.timerThreads.pop().stop()
            return True
        return False

    def _stop_all_timers(self):
        if not self._stop_timer():
            return False
        while self._stop_timer():
            pass
        return True

    def _start_timer(self, match, command):
        if match:
            action = match.group(command.action_group)
            try:
                hours = match.group(command.hours_group)
                and_1 = match.group(command.and_group_1)
                minutes = match.group(command.minutes_group)
                and_2 = match.group(command.and_group_2)
                seconds = match.group(command.seconds_group)

                self.speak_callback("OK", *self._create_responses(action, hours, and_1, minutes, and_2, seconds))

                if hours is not None and hours != "":
                    hours_val = word_to_num(hours)
                else:
                    hours_val = 0
                if minutes is not None and minutes != "":
                    minutes_val = word_to_num(minutes)
                else:
                    minutes_val = 0
                if seconds is not None and seconds != "":
                    seconds_val = word_to_num(seconds)
                else:
                    seconds_val = 0
                self._start_timer_thread(hours_val, minutes_val, seconds_val)

            except ValueError:
                self.speak_callback(f"I'm sorry, that's not a timer I can {action}")

    def _start_timer_thread(self, hours, minutes, seconds):
        self.timerThreads.append(TimerThread(hours * 3600 + minutes * 60 + seconds, self.timerThreads.remove))

    def _create_responses(self, action, hours, and_1, minutes, and_2, seconds):
        response_start = ""
        if action == "start":
            response_start += "starting "
        else:
            response_start += "setting "
        response_start += "timer for"

        response_time = ""
        if hours is not None and hours != "":
            response_time += hours
            response_time += " hour"
        if and_1 is not None and and_1 != "":
            response_time += and_1
        if minutes is not None and minutes != "":
            response_time += " "
            response_time += minutes
            response_time += " minutes"
        if and_2 is not None and and_2 != "":
            response_time += and_2
        if seconds is not None and seconds != "":
            response_time += " "
            response_time += seconds
            response_time += " seconds"

        return response_start.strip(), response_time.strip()
