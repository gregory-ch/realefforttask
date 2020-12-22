from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


# variables for all templates
# --------------------------------------------------------------------------------------------------------------------
# def vars_for_all_templates(self):
#     return {
#         'prob_hi': "{0:.1f}".format(Constants.probability) + "%",
#         'prob_lo': "{0:.1f}".format(100 - Constants.probability) + "%"
#     }


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1
    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        num_lotteries = Constants.num_lotteries + 1 if Constants.risk_loving else Constants.num_lotteries
        num_rounds = Constants.num_rounds
        return {
            'num_lotteries': num_lotteries,
            'num_rounds': num_rounds
        }


# ******************************************************************************************************************** #
# *** PAGE DECISION *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form model
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'

    # form fields
    # ----------------------------------------------------------------------------------------------------------------
    form_fields = ['lottery_choice']

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        return {
            'lotteries': self.player.participant.vars['scl_lotteries_ega']
        }

    # set payoff
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):
        self.player.set_payoffs()


# ******************************************************************************************************************** #
# *** PAGE RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        lottery = (
            self.player.lottery_choice,
            self.player.outcome_lo,
            self.player.outcome_hi,
            self.player.p_lo,
            self.player.p_hi,
            self.player.p_range_lo,
            self.player.p_range_hi,
        )

        return {
            'lottery_choice': self.player.lottery_choice,
            'outcome_to_pay': self.player.outcome_to_pay,
            'index':          self.player.participant.vars['scl_lotteries_ega'].index(lottery) + 1,
            'hi_lo':          "B" if self.player.outcome_to_pay == "high" else "A",
            'lottery':        [lottery]
        }


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision]

if Constants.instructions:
    page_sequence.insert(0, Instructions)

if Constants.results:
    page_sequence.append(Results)
