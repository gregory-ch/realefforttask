from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Intro(Page):
    pass
    def is_displayed(self):
        return self.round_number == 1
    def vars_for_template(self):

        num_rounds = Constants.num_rounds
        return {

            'num_rounds': num_rounds
        }

class ChoosingDiff(Page):
    form_model = 'player'
    form_fields = ['difficulty']
    timeout_submission = {'difficulty': 5}

    def vars_for_template(self):
        frm = self.get_form()
        f = frm['difficulty']

        return {'data': zip(Constants.diff_choices, f)}


class WorkPage(Page):
    timer_text = 'Time left to complete this round:'
    timeout_seconds = Constants.task_time

    def is_displayed(self) -> bool:
        return self.player.tasks.filter(answer__isnull=False).count() < 1

    def vars_for_template(self):
        return {"task": self.player.get_task()}

    def before_next_page(self):
        self.player.dump_tasks()
        self.player.set_payoff()


class Results(Page):
    ...


page_sequence = [
    Intro,
    ChoosingDiff,
    WorkPage,
    Results,
]
